@echo off

IF NOT "%1"=="" (
        SET PHONE=%1
        SHIFT
	
	IF NOT "%2"=="" (
        	SET SMS=%2
        	SHIFT
		
		adb shell am start -a android.intent.action.SENDTO -d sms:%PHONE% --es sms_body %SMS% --ez exit_on_sent true
		adb shell input keyevent 61 
		adb shell input keyevent 61
		adb shell input keyevent 66
    	)
    )    
)