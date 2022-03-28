var bucketName ="labstack-prewarm-221db358-6195-4f3c-8e1-webbucket-1hv29kifqrau9"; // 1. Enter your bucket name
var Bucketregion = "us-east-1"; // 2. Enter Bucket region
var IdentityPoolId = "us-east-1:4258f838-8e4d-41e0-8333-0d0e57c7f0d5"; // 3. Enter Identity Pool Id
var UserPoolId = "us-east-1_Qeg2h8c96"; // 4. Enter User Pool Id
var DynamoTableName = "LabStack-prewarm-221db358-6195-4f3c-8e16-8ca13ae27470-uK3GWxFPSAooSVwAXTLuhd-2-DynamoTableName-19YRDVVRK4OV1"; // 5. Enter DynamoDB Table Name
// get id_token from the url post login
var urlLocator = window.location.href;
var remURL = urlLocator.split("#")[1];
var idTokenNameVal = remURL.split("&")[0];
var idToken = idTokenNameVal.split("=")[1];

console.log(idToken); //
alert("ID Token : " + idToken); //

results.innerHTML = "Token extract from the URL: " + idToken; // Integrating a User Pool with an Identity Pool
var loginKey = "cognito-idp." + Bucketregion + ".amazonaws.com/" + UserPoolId; // set up user credentials
AWS.config.update({
  region: Bucketregion,
  credentials: new AWS.CognitoIdentityCredentials({
    IdentityPoolId: IdentityPoolId,
    Logins: { [loginKey]: idToken },
  }),
});
