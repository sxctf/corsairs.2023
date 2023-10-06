async function mainAjaxFunc(path, method, data, headers) {
    return $.ajax({
        url: path,
        method: method,
        data: JSON.stringify(data),
        headers: headers
    });
}


$(document).on('click', '.sign-in-btn', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    mainAjaxFunc("/auth-page/fragment", "GET").then(function (result) {
        $('body').html(result);
        window.history.pushState(null, "", "/auth-page");
    })
});


$(document).on('click', '.octagon-block', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    $('.octagon-background-container').css("background-color", "#00a5ff");
    $(this).parent().css("background-color", "#00ff9e");

    let locationData = await mainAjaxFunc("/location/data/" + getActiveLocation(),
        "GET");
    $('.search-results').html(locationData)
});

$(document).on('click', '#registration-btn', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    let username = $('.username-input').eq(0).val();
    let password = $('.password-input').eq(0).val();
    let userObject = {
        username: username,
        password: password
    };
    mainAjaxFunc("/user/create", "POST", userObject,
        {'Content-Type': 'application/json'}).then(function (result) {
        $('#text-container').empty().html(result);
    }).catch(function (error) {
        $('#text-container').empty().html("Ошибка: " + error.responseText);
    });
});
$(document).on('click', '.add-container-btn', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    let locationName = getActiveLocation();
    let treasure = $('.add-container-input').val();
    let data = {
        treasure: treasure,
        locationName: locationName
    };
    if (locationName === "") {
        alert("Выберите локацию!")
    } else {
        await mainAjaxFunc("/container/save",
            "POST", data, {'Content-Type': 'application/json'});
    }
    let locationData = await mainAjaxFunc("/location/data/" + getActiveLocation(),
        "GET");
    $('.search-results').html(locationData)
});

$(document).on('click', '.log-out', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    await mainAjaxFunc("/logout", "GET").then(function () {
        mainAjaxFunc("/auth-page/fragment", "GET").then(function (result) {
            $('body').html(result);
            window.history.pushState(null, "", "/auth-page");
        })
    });
});
$('body').on('click', '.turn-to-registration-btn', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    mainAjaxFunc("/registration", "GET").then(function (result) {
        $('body').html(result);
        window.history.pushState(null, "", "/registration");
    });
});
$(document).on('click', '.turn-to-map', async function (e) {
    e.preventDefault();
    e.stopPropagation();
    window.location.href = "/";
});

function getActiveLocation() {
    let tags = $('.octagon-background-container');
    let activeLocationName = "";
    $.each(tags, function (index, value) {
        if ($(value).css('background-color') === 'rgb(0, 255, 158)') {
            activeLocationName = $(value).attr("name");
        }
    })
    return activeLocationName;
}


