Attribute VB_Name = "getBoldChar"
Option Explicit

Sub get_Bold_Characters()

    Dim i, j
    Dim myChar
    Dim strText As String
    Dim intStart
    
    For i = 2 To Range("E65536").End(xlUp).Row
        If Cells(i, 5) <> "" Then
            strText = ""
            intStart = 0
            For j = 1 To Len(Cells(i, 5).Value)
                If Range("E" & i).Characters(j, 1).Font.Bold = False Then
                    intStart = 0
                Else
                    If intStart = 0 Then
                        strText = strText & "," & Range("E" & i).Characters(j, 1).Text
                    Else
                        strText = strText & Range("E" & i).Characters(j, 1).Text
                    End If
                    intStart = 1
                End If
            Next j
            If Left(strText, 1) = "," Then strText = Mid(strText, 2, Len(strText) - 1)
            Cells(i, 6) = strText
        End If
    Next i

End Sub
