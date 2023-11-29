#!/usr/bin/env python
# coding=utf-8

"""
Author       : Kofi
Date         : 2023-11-11 09:25:34
LastEditors  : Kofi
LastEditTime : 2023-11-11 09:29:11
Description  : sqlite3 工具类,主要用于合并数据库,保持文件一致性
"""

import sqlite3, os, time


class Sqlite3Helper:
    def __init__(self, file) -> None:
        self.file = file
        self.current_conn = sqlite3.connect(self.file)
        self.current_cursor = self.current_conn.cursor()

    def is_db_file(self, filePath):
        if os.path.exists(filePath):
            db_extensions = ["db", "sqlite", "sqlite3"]
            file_extension = filePath.lower().rsplit(".", 1)[-1]
            return file_extension in db_extensions
        else:
            raise Exception("文件不存在")

    def merge(self, sourceFile):
        if self.is_db_file(sourceFile):
            source_conn = sqlite3.connect(sourceFile)
            source_cursor = source_conn.cursor()

            # 获取所有表格名称
            source_cursor.execute(
                "SELECT name,sql FROM sqlite_master WHERE type='table';"
            )
            tables = source_cursor.fetchall()

            # 统计新增表的数量、每个表的新增数量和修改数量
            table_count = 0
            table_stats = {}

            start_time = time.time()

            # 遍历源数据库中的表
            for table_name, table_sql in tables:
                # 检查当前数据库中是否存在同名表
                self.current_cursor.execute(
                    f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
                )
                existing_table = self.current_cursor.fetchone()

                # 如果不存在同名表，则创建表并导入数据
                if not existing_table:
                    self.current_cursor.execute(table_sql)
                    self.current_cursor.execute(f"SELECT * FROM {table_name};")
                    source_data = self.current_cursor.fetchall()
                    self.current_cursor.executemany(
                        f"INSERT INTO {table_name} VALUES ({','.join(['?'] * len(source_data[0]))});",
                        source_data,
                    )
                    self.current_conn.commit()

                    # 更新表数量和新增数据数量
                    table_count += 1
                    table_stats[table_name] = {"新增数量": len(source_data), "修改数量": 0}

                # 如果存在同名表，则导入数据并检查更新
                else:
                    self.current_cursor.execute(f"SELECT * FROM {table_name};")
                    current_data = self.current_cursor.fetchall()
                    current_columns = [
                        column[1] for column in self.current_cursor.description
                    ]

                    source_cursor.execute(f"SELECT * FROM {table_name};")
                    source_data = source_cursor.fetchall()
                    source_columns = [column[0] for column in source_cursor.description]

                    # 获取主键或唯一索引列的索引
                    unique_indices = []
                    for i, column in enumerate(current_columns):
                        self.current_cursor.execute(f"PRAGMA index_list({table_name});")
                        indices = self.current_cursor.fetchall()
                        for index in indices:
                            index_name = index[1]
                            index_info = self.current_cursor.execute(
                                f"PRAGMA index_info({index_name});"
                            ).fetchall()
                            if any(column in column_info for column_info in index_info):
                                unique_indices.append(i)

                    # 遍历源数据行
                    for source_row in source_data:
                        is_new_row = True

                        # 遍历当前数据行
                        for current_row in current_data:
                            is_conflict = True

                            # 检查是否存在主键或唯一索引冲突
                            for index in unique_indices:
                                if source_row[index] != current_row[index]:
                                    is_conflict = False
                                    break

                            # 如果存在冲突，则进行数据比较并更新
                            if is_conflict:
                                # 如果当前数据存在updated_at字段，且源数据较新，则更新当前数据
                                if (
                                    "updated_at" in source_columns
                                    and source_row[source_columns.index("updated_at")]
                                    > current_row[source_columns.index("updated_at")]
                                ):
                                    update_sql = f"UPDATE {table_name} SET "

                                    for i in range(len(current_columns)):
                                        update_sql += f"{current_columns[i]}=?, "

                                    update_sql = update_sql.rstrip(", ")
                                    update_sql += f" WHERE "

                                    for i in range(len(unique_indices)):
                                        update_sql += f"{current_columns[unique_indices[i]]}=? AND "

                                    update_sql = update_sql.rstrip(" AND ")

                                    source_row.extend(source_row[: len(unique_indices)])
                                    self.current_cursor.execute(
                                        update_sql,
                                        source_row,
                                    )

                                    # 更新修改数量
                                    if table_name in table_stats:
                                        table_stats[table_name]["修改数量"] += 1
                                    else:
                                        table_stats[table_name] = {"新增数量": 0, "修改数量": 1}

                                is_new_row = False
                                break

                        # 如果是新数据行，则插入到当前表格
                        if is_new_row:
                            insert_sql = f"INSERT INTO {table_name} VALUES ("

                            for _ in range(len(current_columns)):
                                insert_sql += "?, "

                            insert_sql = insert_sql.rstrip(", ")
                            insert_sql += ");"

                            self.current_cursor.execute(insert_sql, source_row)

                            # 更新新增数量
                            if table_name in table_stats:
                                table_stats[table_name]["新增数量"] += 1
                            else:
                                table_stats[table_name] = {"新增数量": 1, "修改数量": 0}

                    # 提交事务
                    self.current_conn.commit()

                    # 更新表数量
                    table_count += 1

        end_time = time.time()
        total_time = end_time - start_time
        return {"total_time": total_time, "new table": table_count, "info": table_stats}
