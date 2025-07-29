Sub WorksheetToJson()
    Dim ws As Worksheet
    Dim json As String
    Dim i As Integer
    Set ws = ActiveSheet
    json = "{\n  \"name\": \"" & ws.Name & "\",\n  \"description\": \"" & ws.Range("A1").Value & "\",\n  \"fields\": ["
    i = 2
    Do While ws.Cells(i, 1).Value <> ""
        json = json & "{\"label\": \"" & ws.Cells(i, 1).Value & "\""
        If ws.Cells(i, 2).Value Like "*;*" Then
            json = json & ", \"type\": \"dropdown\", \"choices\": ["
            Dim parts As Variant
            parts = Split(ws.Cells(i, 2).Value, ";")
            Dim j As Integer
            For j = LBound(parts) To UBound(parts)
                json = json & "\"" & Trim(parts(j)) & "\""
                If j < UBound(parts) Then json = json & ", "
            Next j
            json = json & "]}"
        Else
            json = json & ", \"type\": \"" & ws.Cells(i, 2).Value & "\"}"
        End If
        i = i + 1
        If ws.Cells(i, 1).Value <> "" Then json = json & ","
    Loop
    json = json & "]\n}"
    Dim fso As Object, fileOut As Object
    Set fso = CreateObject("Scripting.FileSystemObject")
    Set fileOut = fso.CreateTextFile(ws.Name & ".json", True)
    fileOut.Write json
    fileOut.Close
End Sub
