Attribute VB_Name = "Menu"
Sub createmMenu()
    On Error Resume Next
    Application.CommandBars("执行").Delete
    Application.CommandBars.Add "执行", 1, , True
    Application.CommandBars("执行").Visible = True
    With Application.CommandBars("执行").Controls
        With .Add(1, , , , True)
            .Caption = "执行"
            .Visible = True
            .Style = msoButtonIconAndCaption
            .FaceId = 50
            .OnAction = "执行"
        End With
    End With
End Sub

Sub deleteMenu()
    On Error Resume Next
    Dim comm
    For Each comm In Application.CommandBars
        comm.Delete
    Next
End Sub


