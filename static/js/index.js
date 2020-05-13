(function(){

	console.log('checkSystemRequirements');
	console.log(JSON.stringify(ZoomMtg.checkSystemRequirements()));
    ZoomMtg.preLoadWasm();
    ZoomMtg.prepareJssdk();
  })();

function startMeeting (API_KEY, meetingNumber, meetingPassword,  joinName) {
    var API_SECRET = '2panFGLxPRYE6SjWjPVjvbV4N5sivTonJaCn';
    var meetConfig = {
        apiKey: API_KEY,
        apiSecret: API_SECRET,
        meetingNumber: meetingNumber,
        userName: joinName,
        passWord: meetingPassword,
        leaveUrl: "https://jiitclassroom.herokuapp.com/",
        role: parseInt(0, 10)
    };


    var signature = ZoomMtg.generateSignature({
        meetingNumber: meetConfig.meetingNumber,
        apiKey: meetConfig.apiKey,
        apiSecret: meetConfig.apiSecret,
        role: meetConfig.role,
        success: function(res){
            console.log("Success");
        }
    });

    ZoomMtg.init({
        leaveUrl: 'https://jiitclassroom.herokuapp.com/',
        isSupportAV: true,
        success: function () {
            ZoomMtg.join(
                {
                    meetingNumber: meetConfig.meetingNumber,
                    userName: meetConfig.userName,
                    signature: signature,
                    apiKey: meetConfig.apiKey,
                    passWord: meetConfig.passWord,
                    success: function(res){
                        console.log('join meeting success');
                    },
                    error: function(res) {
                        console.log(res);
                    }
                }
            );
        },
        error: function(res) {
            console.log(res);
        }
    });

}

// Function end


