input:=""

Loop 

{

  Input, in, IL1, {Enter}

  EL:=ErrorLevel

  input.=in

  ToolTip, % input

} until (EL!="Max")

MsgBox % input

ExitApp