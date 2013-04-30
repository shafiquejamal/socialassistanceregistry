rm -r ~/projects/av4repo_old
mv ~/projects/av4repo ~/projects/av4repo_old
cp -vr ~/html/av4repo ~/projects
rm -r ~/html/av4repo
django-admin.py collectstatic --settings=av4.settings.testingserver