#### RaspAutomata
A Raspberry Pi based, server monitoring and configuration environment

### Schematic
Agent is the key part of the program, utilizing data sensing.
Controller is to regularly call agents, and send reports according to the Reporting Policy.

Agent <-> Agent Helper <-> Storation
                |
                |
Web UI <-> Controller <-> Console UI

Also, there is a separate logging daemon available.

### UI Implementation
```
UI is implemented by curses library
(Unix Only)
                                   m/M       +-------------+
                              +------------->+RaspAuto Mgr.|
                              |              +-------------+
                          Exit|    r/R       +-------------+
                            ^ +------------->+Remote Conn. |
                         e/E| |    b/B       +-------------+
                            | |
+---------+   h/H      +------+--+    i/I    +-------------+
|Help page<------------+Overview +----------->Detailed Info|
+---------+   b/B      +-----^---+    b/B    +-------------+
                            ||
                         s/S||b/B
                            ||
                            ||
                       +----v--------+
                       |Detailed Stat|
                       +-------------+

Query: Processes that can be excuted very fast
Agent: Could schedule Query and store it into db; plugins for daemon
```

### Script File Description
Script file is used to record session operations and used for audit.
the script file format:
```
struct script_file {
	// Time, in seconds
	uint64 starttime;
	uint64 stoptime;
	// The $TERM variable
	char term[50];
	uint32 term_x;
	uint32 term_y;
}
```
Followed by a bunch of records:
```
struct script_record {
	// Milliseconds before last packet; **49h at most**
	uint32 msec;
	char seq[512];
}
