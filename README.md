# Study-Python

First project - "Module to upload some files to the remote server"

Description:
1. Write module to upload some files to the remote server. 
2. Uploading should be done in parallel. 
3. Python multiprocessing module should be used.
4. It should be a method to stop uploading and interrupt all uploading process.
5. Real uploading is not part of this task, use some dummy function for emulate upload.

Input data:
List of files to upload
Maximum number of parallel uploading process
Queue for passing progress to the caller

Output data:
Uploading progress
Final uploading report (uploaded files and not uploaded)