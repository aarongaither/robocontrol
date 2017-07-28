# robocontrol
Keyboard shortcuts for Nordson EFD EV series Robots

### Raison d'etre
Nordson EFD EV series robots only have two methods for programming new path.
* Teach Pendant - An additional piece of equipment (which is essentially a trackball attached via serial) This equipment suffers from added expense and inherently slow/dangerous axis switching.
* Point and Click GUI - Which this interface avoids the axis switching concerns, it poses a new one. How is an operator to watch both the input screen and the armature simultaneously?

This program solves the aforementioned problem by converting configurable keyboard shortcuts into mouce move and click events.

### Implementation
When the robocontrol script is run it hooks into the windows HID controller and automatically intercepts all keyboard input. If the key event does not match a corresponding ID in the app configuration file, then the event is passed on to windows to process normally. If the event does match, then the app will hijack the input and perform the prescribed action defined in the config.

### Usage
All controls can be configured via the configuration file (ext .ini).

*Quit: Esc
*Toggle Hook: Scroll Lock
*Display Commands: Pause/Break
*Increase Speed: Home
*Decrease Speed: Insert
*Dummy Point: End
*Drop Point: Delete
*Y-: Up
*Y+: Down
*X-: Left
*X+: Right
*Z-: Prior (Page Up)
*Z+: Next (Page Down)