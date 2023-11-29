The shell scripts in this directory use the `ucampurestorage` package in pypi.

##### Script Descriptions

1. pure_create_volume
    - Creates a snapshot of a Pure storage volume.

    - Example:-
    ```
        pure_create_volume -n TEST123 -s 1T -k /path/to/secrets.json
    ```

2. pure_eradicate_destroyed_volume
    - Eradicates the destroyed Pure storage volumes listed in a file OR (exclusive) the destroyed volumes listed in a set of files under a given directory that are older than n number of days. The age of files is uniquely determined by the date used to name them.  May not work when "SafeMode" is enabled.

    - Example:-
    ```
    1. pure_eradicate_destroyed_volume -o by_file -r /path/to/destroyed/vols/file -k /path/to/secrets.json
    2. pure_eradicate_destroyed_volume -o by_age -p /path/to/destroyed/vols -n 7 -k /path/to/secrets.json
    ```

3. pure_record_destroyed_volume
    - Saves the list of destroyed Pure storage volumes in files.

    - Example:-
    ```
        pure_record_destroyed_volume -o /path/to/dir/ -k /path/to/secrets.json
    ```

4. pure_unmap_volume
    - Unmaps a Pure storage volume.

    - Example:-
    ```
        1. pure_unmap_volume -n Test123 -k /path/to/secrets.json
        2. pure_unmap_volume -w 123455 -k /path/to/secrets.json
        3. pure_unmap_volume -p /t123 -k /path/to/secrets.json

    ```

5. pure_create_snapshot
    - Creates a snapshot of a Pure storage volume.
      - Note: the snapshot information will be recorded in a `/opt/pureutils/snapshot`

    - Example:-
    ```
        pure_create_snapshot -s TEST123 -l "snap01"  -k /path/to/secrets.json
    ```

6. pure_delete_volume
    - Deletes a Pure storage volume (sends to the "recycle bin").

    - Example:-
     ```
        pure_delete_volume -n TEST123 -k /path/to/secrets.json
    ```

8. pure_map_volume
    - Maps a Pure storage volume and mounts it on the local server, optionally formatting it as ext4.

    - Example:-
    ```
        For new volume : pure_map_volume -n TEST121 -p /t1 -x 1 -k /path/to/secrets.json
        For clone volume: pure_map_volume -n TEST121 -p /t1 -x 0 -k /path/to/secrets.json
    ```

9. pure_replace_volume
    - Clones one Pure storage volume (source/"gold image") and mounts it in place of another Pure storage volume (dest/"target"). The replaced Pure storage volume is then deleted.

    - Example:-
    ```
        pure_replace_volume -g /d16 -t /d17 -k /path/to/secrets.json
    ```

10. pure_eradicate_volume
    - Eradicates a Pure storage volume.  May not work when "SafeMode" is enabled.

    - Example:-
     ```
        pure_eradicate_volume -n TEST123 -k /path/to/secrets.json
    ```

11. pure_expire_snapshot_deletion
    - It will delete the snapshot, if the expiration date occurred.
    - This script will read the files with extension `.pure` present in a `/opt/pureutils/snapshot`

    - Example:
     ```
        pure_expire_snapshot_deletion -k /path/to/secrets.json
    ```
1. pure_clone_volume
    - Creates a clone of a Pure storage volume. The clone will be mapped to the local server and mounted on the desired mount point.  Creating the mount point if it doesn't exist.

    - Example:-
    ```
        pure_clone_volume -n clone_name -s source_name -p /t10 -k /path/to/secrets.json
    ```
