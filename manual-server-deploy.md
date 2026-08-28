## Server Update
This is for instances in which there have been only minor changes to the tasks and no secrets have been changed.

1. Go to the project folder, and compress the theproject_tasks to a zip archive.

2. Move the zip archive to Downloads

3. Add the ssh-key for the server with the usual annoying eval "$(ssh-agent)" and add the ssh-key for this server.

4. Now, ssh into the server

```bash
ssh ics@<SERVER-IP-ADDRESS>
```

5. 
Remove this if it exists
```bash
rm theproject_tasks.zip
```

6. Exit from ssh, but in the same shell:
```bash
scp /mnt/c/Users/AlexLowe/Downloads/theproject_tasks.zip ics@<SERVER-IP-ADDRESS>:~/ 
```
It's small and it will take almost no time.

7. In that same shell, ssh again.

8. Run this to replace and unzip the tasks
```bash
cd theproject-master && \
mv theproject_tasks theproject_tasks_backup && \
cp ../theproject_tasks.zip theproject_tasks.zip && \
unzip -q theproject_tasks.zip && \
rm theproject_tasks.zip && \
cd ~/
```

9. Run whatever tasks you want. When it looks like it's working,
```bash
cd theproject-master && \
rm -rf theproject_tasks_backup

