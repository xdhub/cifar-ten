#Strive for the perfect commit message

The commit history should read like a story about the code.


##Why
Reduce the amount of time it takes to re-establish context in the code.  This makes maintainability and reviewing smoother.

An additional opportunity to explain code intent and keep comments and their rotting out of the code base.

With github this commit history is also part of the feed.  We want to keep this feed clean and valuable.  
The feed give us an opportunity to stay up to date with what everyone on the team is doing even if were not on the same project.

##Format
	Summarize clearly in one short line what the commit is about
	
	Describe the problem or feature the commit full-fills. 
	Explain the forces that shaped the commit, it could
	be a technical issue, business reason, etc.


###Example
	Drag and drop to choose between drone weapon

	Use a b-tree vs a kd-tree because all 
	items sit on the same x position.  Move the array
	manipulation methods to a new file for discover
	ability and re-usability.

	The drop transition is awkwardly slow, this was
	requirement by the business to emphasize the
	magnitude of the user action.


##DO
- leave the second line blank.
- always put a carriage return after your summary line.  This makes *'git log'* prettier. some ways [here](http://stackoverflow.com/questions/5064563/add-line-break-to-git-commit-m-from-command-line).
- squash and re-arrange your local commits to tell a more linear story. 
- write in [imperative mood](http://en.wikipedia.org/wiki/Irrealis_mood#Imperative).  
- The summary line should be from the perspective of the program not the programmer.
- Details can be from programmer perspective.


##DON'T
- put a period after the summary sentence.  This makes  *'git log'* prettier.

##SMELLS
- if it's difficult to write a concise summary message it may be because your commit includes to many logical changes.  

Reference: [erlang](https://github.com/erlang/otp/wiki/writing-good-commit-messages), [Who-T](http://who-t.blogspot.com/2009/12/on-commit-messages.html), [lkml](https://lkml.org/)
