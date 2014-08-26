var twitter_socket;

$('#filter_submit').click(function() {
    var filter_keyword = $('#filter_keyword_input').val()
    twitter_socket_start(filter_keyword);
});

function twitter_socket_start(filter_keyword) {
    if (twitter_socket) {
        twitter_socket.send(JSON.stringify({'change_keyword': true, 'keyword_filter': filter_keyword}));
        $('#tweets').empty()
    }
    else {
        twitter_socket = new WebSocket('ws://127.0.0.1:8080/twitter');
        twitter_socket.onopen = function () {
            twitter_socket.send(JSON.stringify({'keyword_filter': filter_keyword}));
        };
        twitter_socket.onmessage = function (s) {
            console.log(s.data);
            data = eval("(" + s.data + ")");
            var div = $("<div class='col-sm-3 content-card'><div class='stream-card'><div class='stream-card-content'><div class='stream-card-content'> " + data.text + "<div class='stream-card-content stream-header'><img src=" + data.user.profile_image_url + "/><h3>" + data.user.screen_name + "</h3></div></div></div></div>");
            $('#tweets').prepend(div);
            setTimeout(get_next_tweet, 1500);
        };
    }
}

function get_next_tweet() {
    twitter_socket.send(JSON.stringify({}));
}