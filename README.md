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
|Help page<------------+O|er|iew +----------->Detailed Info|
+---------+   b/B      +-----^---+    b/B    +-------------+
                            ||
                         s/S||b/B
                            ||
                            ||
                       +----v--------+
                       |Detailed Stat|
                       +-------------+
```