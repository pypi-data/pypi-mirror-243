import os
import shutil
import sqlite3
from typing import Optional, List


class Scanner:
    """Scan the file system for duplicate files"""

    def __init__(self, *, db_path: str, clean=False):
        """
        Scanner for duplicate file detection
        :param db_path: Path to the sqlite3 database file
        :param clean: If true then delete any existing database file before starting
        """
        if clean is True:
            if os.path.exists(db_path):
                os.remove(db_path)
        self._con = sqlite3.connect(db_path)
        self._cur = self._con.cursor()
        self._cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS DirInfo
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
            ,path TEXT NOT NULL
            ,UNIQUE (path)
            )
            '''
        )
        self._cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS FileInfo
            (file_size INTEGER NOT NULL
            ,dir_id INTEGER NOT NULL
            ,file_name TEXT NOT NULL
            ,PRIMARY KEY (dir_id, file_name)
            )
            '''
        )
        self._cur.execute(
            '''
            CREATE INDEX IF NOT EXISTS FileSizeNdx ON FileInfo (file_size)
            '''
        )
        self._con.commit()

    def scan(
            self, *,
            dir_path: str,
            extensions: Optional[List[str]]=None
    ):
        """
        Scan directory and subdirectories for master files
        :param dir_path: Path to directory to start the scan in
        :param extensions: Optional filename extensions to scan
        """
        print(f'Scan {dir_path} for masters')
        file_count = 0
        total_size = 0
        for root_dir, dir_names, file_names in os.walk(dir_path):
            eligible_file_names = self._eligible_file_names(root_dir, file_names, extensions)
            if len(eligible_file_names) > 0:
                dir_id = self._record_directory(root_dir)
                for file_name in eligible_file_names:
                    file_path = os.path.join(root_dir, file_name)
                    stat_info = os.stat(file_path)
                    file_size = stat_info.st_size
                    file_count += 1
                    total_size += file_size
                    self._cur.execute(
                        '''INSERT INTO FileInfo (file_size, dir_id, file_name) VALUES (?,?,?)''',
                        (file_size, dir_id, file_name)
                    )
            self._con.commit()
        print(f'{file_count:,} files scanned with {total_size:,} bytes')
        return {
            'files': {
                'count': file_count,
                'size': total_size,
            }
        }

    def _record_directory(self, root_dir: str) -> int:
        self._cur.execute(
            '''INSERT OR IGNORE INTO DirInfo (path) VALUES (?)''',
            (root_dir,)
        )
        self._cur.execute(
            '''SELECT id FROM DirInfo WHERE path = ?''',
            (root_dir,)
        )
        dir_id = self._cur.fetchone()[0]
        self._cur.execute(
            '''DELETE FROM FileInfo WHERE dir_id = ?''',
            (dir_id,)
        )
        return dir_id

    @staticmethod
    def _eligible_file_names(root_dir: str, file_names: List[str], extensions: Optional[List[str]]):
        eligible_file_names = []
        for file_name in file_names:
            if extensions is not None:
                _f, _ext = os.path.splitext(file_name)
                if _ext.startswith('.'):
                    _ext = _ext[1:]
                if _ext.lower() not in extensions:
                    continue
            file_path = os.path.join(root_dir, file_name)
            if os.path.islink(file_path):
                continue
            eligible_file_names.append(file_name)
        return eligible_file_names

    def clean(
            self, *,
            dir_path: str,
            extensions: Optional[List[str]]=None,
            remove_dups=False,
            trash_dups=False,
            archive_to=None
    ):
        """
        Scan directory and subdirectories for duplicate files
        :param dir_path: Path to directory to start the scan in
        :param extensions: Optional filename extensions to scan
        :param remove_dups: If true then remove the duplicate files
        :param archive_to: Path to archive duplicate files to
        """
        print(f'Scan {dir_path} for duplicates')
        dups_count = 0
        dups_size = 0
        files_count = 0
        files_size = 0
        for root_dir, dir_names, file_names in os.walk(dir_path):
            self._cur.execute(
                '''SELECT id FROM DirInfo WHERE path = ?''',
                (root_dir,)
            )
            if self._cur.fetchone() is not None:
                continue
            eligible_file_names = self._eligible_file_names(root_dir, file_names, extensions)
            if len(eligible_file_names) > 0:
                for file_name in eligible_file_names:
                    files_count += 1
                    target_file_path = os.path.join(root_dir, file_name)
                    stat_info = os.stat(target_file_path)
                    file_size = stat_info.st_size
                    files_size += file_size
                    self._cur.execute(
                        '''
                        SELECT path, file_name 
                        FROM FileInfo fi 
                        JOIN DirInfo di ON di.id = fi.dir_id 
                        WHERE file_size = ?
                        ''',
                        (file_size,)
                    )
                    masters = self._cur.fetchall()
                    for row in masters:
                        master_file_path = os.path.join(row[0], row[1])
                        if self._compare_files(target_file_path, master_file_path):
                            dups_count += 1
                            print(f'{dups_count:,} : {target_file_path} (size {file_size:,})')
                            print(f'  Master {master_file_path}')
                            if archive_to is not None:
                                self._archive_file(target_file_path, dir_path, archive_to)
                            elif trash_dups is True:
                                self._trash_file(target_file_path)
                            elif remove_dups is True:
                                self._remove_file(target_file_path)
                            else:
                                print(f'  Would remove duplicate file {target_file_path}')
                            dups_size += file_size
                            break
        print(f'{dups_count:,} of {files_count:,} duplicate files occupying {dups_size:,} bytes')
        return {
            'duplicates': {
                'count': dups_count,
                'size': dups_size,
            },
            'files': {
                'count': files_count,
                'size': files_size,
            },
        }

    @staticmethod
    def _remove_file(target_file_path):
        print(f'  Remove duplicate file {target_file_path}')
        os.remove(target_file_path)

    def _trash_file(self, target_file_path):
        trash_files_path = self.trash_directory()
        if trash_files_path is not None:
            file_name = os.path.basename(target_file_path)
            trash_file_path = os.path.join(trash_files_path, file_name)
            print(f'  Trash duplicate file {target_file_path}')
            shutil.move(target_file_path, trash_file_path)

    @staticmethod
    def trash_directory():
        home = os.getenv('HOME')
        local = os.path.join(home, '.local')
        share = os.path.join(local, 'share')
        trash = os.path.join(share, 'Trash')
        trash_files_path = os.path.join(trash, 'files')
        if os.path.exists(trash_files_path):
            return trash_files_path
        return None

    @staticmethod
    def _archive_file(target_file_path, dir_path, archive_to):
        target_file_suffix = target_file_path[len(dir_path):]
        while target_file_suffix.startswith('/'):
            target_file_suffix = target_file_suffix[1:]
        archive_file_path = os.path.join(archive_to, target_file_suffix)
        archive_dir_path = os.path.dirname(archive_file_path)
        if not os.path.exists(archive_dir_path):
            os.makedirs(archive_dir_path, mode=0o700, exist_ok=False)
        print(f'  Archive duplicate file to {archive_file_path}')
        os.rename(target_file_path, archive_file_path)

    @staticmethod
    def _compare_files(source_file_path: str, target_file_path: str) -> bool:
        source_fp = os.open(source_file_path, os.O_RDONLY)
        target_fp = os.open(target_file_path, os.O_RDONLY)
        source_bytes = os.read(source_fp, 1000)
        target_bytes = os.read(target_fp, 1000)
        while source_bytes == target_bytes and len(source_bytes) > 0:
            source_bytes = os.read(source_fp, 1000)
            target_bytes = os.read(target_fp, 1000)
        os.close(source_fp)
        os.close(target_fp)
        if source_bytes != target_bytes:
            return False
        return True
