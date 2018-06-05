var appManager = new Vue({
    el: '#mfaApp',
    delimiters: ['[[', ']]'],
    data: {
        message: 'Welcome your token=D36A4RH5django' 
    }
});


var dataCounter = new Vue({
    el: '#dataUsed',
    delimiters: ['[[', ']]'],
    data: {
        dataUsed: 0,
        maxDataAllowed: 0
    },
    mounted: loadDataCounter,
    methods: {
        loadDataCounter: loadDataCounter,
    }
});

var fileView = new Vue({
    el: '#fileDetailsModal',
    delimiters: ['[[', ']]'],
    data: {
        file: {
            id: null,
            name: "",
            size: 0,
            link: '',
        },
        searchIsActive: false,
        searchUserResults: [],
        userSelected: {
            id: null,
            name: null
        }
    },
    methods: {
        resetSearch: function() {
            this.searchIsActive = false;
            this.searchUserResults = [];
            this.userSelected = {
                id: null,
                name: null
            };
        }
    }
});


Vue.component('dir-item', {
    template: '#dirTemplate',
    delimiters: ['[[', ']]'],
    props: {
        model: Object
    },
});


var moveVue = new Vue({
    el: '#moveModal',
    delimiters: ['[[', ']]'],
    data: {
        id: null,
        name: null,
        type: null,
        tree: {}
    }
});


$('#fileDetailsModal').on('hidden.bs.modal', function (e) {
    $('#fileDetailsModal .modal-body #fileContent').html('');
    fileView.resetSearch();
});

$('#uploadModal').on('hidden.bs.modal', function (e) {
    $('#uploadFileName').html('');
    $('#dropbox').removeClass("drapActive");
    $("#uploadInput").val("");
    $('#uploadProgress').hide()
});

$('#newDirModal').on('show.bs.modal', function (e) {
    $('#newDirName').val('');
});

$('#publicShareModal').on('hidden.bs.modal', function (e) {
    $('#publicShareModal .copyBtn').text('Copy').removeClass('btn-success').addClass('btn-outline-primary');
});

$('#dropbox').on("dragenter", function (e) {
    e.preventDefault();
    $('#dropbox').addClass("drapActive");
});

$('#dropbox').on("dragleave", function (e) {
    e.preventDefault();
    $('#dropbox').removeClass("drapActive");
});
$(document).on("dragover", function (e) {
    e.preventDefault();
});
$(document).on("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $('#dropbox').addClass("drapActive");
    var files = e.originalEvent.dataTransfer.files;
    $('#uploadFileName').text(files[0].name);
    $("#uploadInput").prop("files", files);
    $('#uploadModal').modal('show');
});

function progress(e) {
    if (e.lengthComputable) {
        var percentage = (e.loaded * 100) / e.total;
    }
}

$("#uploadBtn").on('click', async function () {
    var reqFileExist = await $.post('/api/file/check_file', JSON.stringify({
        'dirId': currentDirId,
        'fname': $("#uploadInput")[0].files[0].name
    }));
    $('#uploadProgress').val(0).show();
    var fileKeyDecrypted = "";
    if (reqFileExist.isFileExist && localStorage.priv_key) {
        var reqFileKey = await $.post('/api/file/get_key', JSON.stringify({
            'fileId': reqFileExist.fileId
        }));
        var privateKey = forge.pki.privateKeyFromPem(localStorage.priv_key);
        fileKeyDecrypted = privateKey.decrypt(forge.util.decode64(reqFileKey.key), 'RSA-OAEP');
    }
    var data = new FormData();
    data.append('file', $("#uploadInput")[0].files[0]);
    data.append('dirId', currentDirId);
    data.append('key', fileKeyDecrypted);
    $.ajax({
        type: 'POST',
        url: '/api/file/upload',
        data: data,
        xhr: function () {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', function (e) {
                    if (e.lengthComputable) {
                        var percentage = (e.loaded * 100) / e.total;
                        $('#uploadProgress').val(percentage);
                    }
                }, false);
            }
            return myXhr;
        },
        cache: false,
        contentType: false,
        processData: false,

        success: function () {
            $('#uploadModal').modal('hide');
            fileManager.openDir(currentDirId);
            dataCounter.loadDataCounter();
        },

        error: function (err) {
            alert(err.responseJSON.message)
        }
    });
});

$('#newDirBtn').on('click', async function () {
    try {
        await $.post('/api/file/add_dir', JSON.stringify({
            name: $('#newDirName').val(),
            dirId: currentDirId
        }));
        $('#newDirModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$('#toggleShare').on('click', function () {
    setTimeout(function () {
        if ($('#toggleShare').attr('aria-pressed') === "true") {
            $('body').addClass('shareIsActive');
        } else {
            $('body').removeClass('shareIsActive');
        }
        fileManager.openDir();
    });
});

$(document).on('click', '.deleteBtn', async function () {
    var id = $(this).attr('data-id');
    var type = $(this).attr('data-type');
    if (!id || !type || !confirm('Are you sure to delete ' + type +' ?')) return;
    try {
        await $.post('/api/file/remove_' + type, JSON.stringify({
            id: id
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('click', '.renameBtn', async function () {
    var type = $(this).attr('data-type');
    var newName = prompt('Enter new  ' + type + ' name');
    var id = $(this).attr('data-id');
    if (!id || !type || !newName) return;
    try {
        await $.post('/api/file/rename_' + type, JSON.stringify({
            id: id,
            name: newName
        }));
        $('#fileDetailsModal').modal('hide');
        fileManager.openDir(currentDirId);
        dataCounter.loadDataCounter();
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('input', '#searchUserInput', async function () {
    fileView.userSelected = {
        id: null,
        name: null
    };
    var val = $(this).val();
    if (!fileView.file.id) return;
    var data = await $.getJSON('/api/user/search?query=' + val);
    fileView.searchUserResults = data.results
});

$(document).on('click', '.searchUserDiv', function () {
    fileView.searchUserResults = [];
    fileView.userSelected.id = $(this).attr('data-userid');
    fileView.userSelected.name = $(this).attr('data-name');
});
$(document).on('click', '#submitShareBtn', async function () {
    try {
        var res = await $.post('/api/share/share', JSON.stringify({
            'elementId': fileView.file.id,
            'targetUserId': fileView.userSelected.id,
            'encryptedKey': 'TODO',
            'read': 1,
            'write': $('#writePerm').is(":checked"),
            'share': $('#sharePerm').is(":checked")
        }));
        fileView.resetSearch();
        alert(res.message)
    } catch (e) {
        alert(e.responseJSON.message)
    }
});

$(document).on('click', '.moveBtn', async function () {
    moveVue.type = $(this).attr('data-type');
    moveVue.id = $(this).attr('data-id');
    moveVue.name = $(this).attr('data-name');
    try {
        var data = await $.getJSON('/api/file/get_tree');
        data.name = 'HOME';
        moveVue.tree = data;
        $('#fileDetailsModal').modal('hide');
        $('#moveModal').modal('show');
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('click', '.dirItem', async function () {
    var target = $(this).attr('data-dirid');
    if (!target || !moveVue.type || !moveVue.id) return;
    try {
        var data = {
            'targetDirId': target
        };
        if (moveVue.type === 'file'){
            data.fileId = moveVue.id
        } else {
            data.dirId = moveVue.id
        }
        await $.post('/api/file/move_' + moveVue.type, JSON.stringify(data));
        $('#moveModal').modal('hide');
        fileManager.openDir(currentDirId);
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('click', '.publicShareBtn', async function () {
    var type = $(this).attr('data-type');
    var id = $(this).attr('data-id');
    try {
        var data = await $.getJSON('/api/share/public?id=' + id + '&type=' + type);
        var link = location.protocol + '//' + location.host + '/api/file/public_download?id=' + id + '&type=' + type + '&permId=' + data.permId
        $('#publicShareModal input').val(link);
        $('#publicShareModal').modal('show');
    } catch (err) {
        alert(err.responseJSON.message);
    }
});

$(document).on('click', '.copyBtn', function () {
    var input = $(this).parent().prevAll('input');
    input.focus();
    input.select();
    try {
        document.execCommand('copy');
        $(this).text('Copied !').removeClass('btn-outline-primary').addClass('btn-success');
    } catch (err) {
        alert("Not supported in your browser")
    }
});