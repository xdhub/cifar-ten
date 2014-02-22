# GitHub Best practices

###Don't
* don't commit generated files - e.x builds, target folders, resharper files, reports, test results, dependencies.
* If one must have hardcoded environment config it should be configured for CI.  e.x [link]build.properties


# Working with GIT

## Team Workflows

* We want to avoid Merge commits
* We want to avoid rebasing the remote master branch

Avoid merge commits using a "topical branches" approach. A topical branch is a local branch which is never pushed remotely.  We commit our work to the local branch rebase/merge that branch to master and push it to the remote.   

### Topical branch

(In this case we use a development branch as the day to day branch)

####Position HEAD on development branch and assure latest:
**git checkout development**    # position the HEAD on the development branch   
**git pull origin development**	# get the latest from remote development branch   

####Create your local
**git checkout -b [topical_branch]**     # create a topical branch and switch to it   
*... work on your feature here .. commit, etc ...*   

####Commit your work to remote
**Run tests**
**git checkout development**     # go back to the development branch when you want to commit your changes from your topical branch onto the development branch   
**git pull origin development**     # prior to rebase/merge, make sure you have the latest from the remote development branch.    
**git checkout [topical_branch]**	# switch back to your topical branch    
**git rebase development**	# rebase commits from development branch into your topical branch.    
**git checkout development**	# switch back to master branch    
**git merge [topical_branch]**	# this will merge the topical_branch into the master branch in Fast-Forward   
**Run Tests**
**git push origin development**	# push into the remote development branch    
**git branch -d [topical_branch]**	# you can now delete your topical branch as it's not needed anymore   

### Seeing differences
#### Commits in the log
**git fetch && git log ..origin/master** # incoming  
**git fetch && git log origin/master..** # outgoing  

#### Diffs
**git checkout master** # change HEAD to master  
**git fetch** # update the local copy (master) of the remote branch (origin/master)  
**git diff master origin/master**  # you can review the changes before you pull them down from the remote (origin/master)  
**git diff [some_branch] origin/master**  # you can do this with branches too.  

*Compare your topical branch with latest in master. In this case you could use 'git pull'. with master checked out.  This would be the same as a 'git fetch' the 'git merge' which will update origin/master and attempt a merge into your local master*    
**git diff [topical_branch] master**  
**git diff --stat --color [topical_branch]..master** # to add some colors and stats 

### Renaming files  
git is case-insensative with filenames.  To change the case of files names you need to  
**git mv some.file temp_SOME.file**  
**git mv temp_SOME.file SOME.file**

## Some references:

* http://progit.org/book/  (a must read to understand git). [see http://git-scm.com/book]
* http://www.randyfay.com/node/91  (a rebase workflow to avoid merge commit disaster)
