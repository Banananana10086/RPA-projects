Attribute VB_Name = "Menu"
Sub createmMenu()
    On Error Resume Next
    Application.CommandBars("ִ��").Delete
    Application.CommandBars.Add "ִ��", 1, , True
    Application.CommandBars("ִ��").Visible = True
    With Application.CommandBars("ִ��").Controls
        With .Add(1, , , , True)
            .Caption = "ִ��"
            .Visible = True
            .Style = msoButtonIconAndCaption
            .FaceId = 50
            .OnAction = "ִ��"
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


