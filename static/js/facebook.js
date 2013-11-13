// A wrapper for the Facebook JS SDK
var Facebook = function () {
  function getAccessToken() {
    if (accessToken === undefined) {
      throw 'User is not authorized.'
    } else {
      return accessToken;
    }
  }

  function get_current_user_profile(callback, fields) {
    if (typeof fields === 'undefined')
      fields = ['name', 'picture'];
    FB.api('/me?fields=' + fields.join() + '&access_token=' + getAccessToken(), function (user) {
      callback(user);
    });
  }

  function get_profile(user_id, callback, fields) {
    if (typeof fields === 'undefined')
      fields = ['name', 'picture'];
    FB.api('/' + user_id + '?fields=' + fields.join() + '&access_token=' + getAccessToken(), function (user) {
      callback(user);
    });
  }

  return {
    me: get_current_user_profile,
    profile: get_profile
  };
};