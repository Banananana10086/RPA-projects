Attribute VB_Name = "Service"
Sub ִ��()
    On Error Resume Next
    Application.ScreenUpdating = False
    Const ForReading = 1, ForWriting = 2, ForAppending = 8, TristateFalse = 0
    Dim wk As Worksheet, resultWk As Worksheet, wb As Workbook, endRow&, i&, file, allfiles, ky, key
    Dim finalRow&, j&, fso As Object, dic As Object, arr
    Dim reusltFolderPath$, rfp$
    Dim sFile As Object, sf As Object
    
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    reusltFolderPath = ThisWorkbook.Path & "\" & "result"
    If Dir(reusltFolderPath, vbDirectory) <> "" Then
        fso.DeleteFolder reusltFolderPath
    End If
    
    If Dir(reusltFolderPath, vbDirectory) = "" Then
        MkDir reusltFolderPath
    End If
    Set wk = ThisWorkbook.Worksheets("����")
    With wk
        endRow = .Cells(.Rows.Count, 1).End(xlUp).Row
        For i = 2 To endRow
            .Range("N" & i) = "" & .Range("B" & i) & Chr(10) & "�����" & .Range("C" & i) & "����" & .Range("G" & i) & .Range("H" & i) & .Range("I" & i) & Chr(10) & Chr(10) & Chr(10) & .Range("B" & i) & Chr(10) & .Range("E" & i) & Chr(10) & .Range("J" & i) & Chr(10) & .Range("K" & i) & Chr(10) & .Range("O" & i) & Chr(10) & .Range("P" & i) & Chr(10) & .Range("Q" & i) & Chr(10) & .Range("R" & i)
            key = "��" & .Range("A" & i) & "��" & .Range("B" & i) & "-----" & .Range("C" & i) & .Range("M" & i)
            rfp = reusltFolderPath & "\" & key
            If Dir(rfp, vbDirectory) = "" Then
                MkDir rfp
            End If
            If Trim(.Range("S" & i)) <> "" And fso.FileExists(.Range("S" & i)) Then ' ���s���Ƿ���Ŀ���ļ�·��
                fso.CopyFile .Range("S" & i), rfp & "\", True
            End If
            Set sFile = fso.CreateTextFile(rfp & "\" & key & ".txt", True) ' �������ı��ļ�
            sFile.WriteLine (.Range("N" & i))
            sFile.Close
            key = ""
        Next
    End With
    
    Set fso = Nothing
    Application.ScreenUpdating = True
    MsgBox "ͳ�����"
End Sub
