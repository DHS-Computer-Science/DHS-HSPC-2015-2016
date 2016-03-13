# Virtual Machine

## Contributors
- Andriy Zasypkin

## Specifications
- Runs Kubuntu 14.04
- outgoing internet is blocked by ufw
  - step 3-6, in the *Running* catagory open one ip(to the submission server)

## Installation
- Use VMPlayer, VirtualBox will need a [hack](http://stackoverflow.com/questions/5906441/how-to-ssh-to-a-virtualbox-guest-externally-through-a-host) and a code change
- That's it

## Running
1. start it up, run the `.vmdk` files with VMPlayer
  - you will be logged in automaticaly(as guest)
2. open the konsole `Ctrl+Alt+T`
3. run the command `su az` (with a space before su) and type the password in
  - should be `zasypkin`
4. be sure that the submission server is up, and take note of its IP
   address(run `ifconfig` on the server)
5. on the vm, in the console that you opened, run `sudo set-ip.sh`
   and type in the same password as in step #3
6. type in the IP address that you should have noted in step #4

## Using it

### Editting
- IDEs
  - eclipse
- GUI text edditors
  - gedit
  - emacs
- CLI edittors
  - vim/vi
  - mcedit
  - nano

### Compiling/Running Java code
- eclipse is an IDE, it does this for you, look it up
- others will need a command line
- compiling
  - open the console
  - use `cd dirname` to change to the directory with your java files
    - use `ls` to list the files and other directories in the current directory
  - run `javac Name.java` in the command line
    (must be in the same dir as Name.java)
- running
  - run `java Name` in the command line - NO EXTENSION, just the class name
    (must be in the same dir as Name.class)
  - you can pipe input/output to/from a text file into std in/out like so
    `java Name < in_file > out_file`
