const connectMethod = 'core.ws_connect';
const uploadMethod = 'files.upload';
const listMethod = 'files.list';
const deleteMethod = 'files.delete';
const loginMethod = 'core.login';
const currentMethod = 'core.current';


const coreLogin = async ({username, password}) => {
    return await request({
        uri: loginMethod,
        method: 'POST',
        data: {
            username: username,
            password: password,
        },
        is_json: true,
    });
}

const coreCurrent = async () => {
    return await request({
        uri: currentMethod,
    })
}

const coreConnect = ({attempt = 0}) => {
    const socket = new WebSocket(`${apiUrl.replace('http://', 'ws://').replace('https://', 'wss://')}/${connectMethod}`);


    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const {kind} = data;

        switch (kind) {
            case 'INITIAL': {
                traceId = data['trace_id'];
                break;
            }
            case 'UPLOAD_PROGRESS': {
                updateUploadProgress(data.upload_id, data.total_size, data.uploaded_size);
                break;
            }
            case 'UPLOAD_FINISH': {
                finishUpload(data['upload_id']);
                break;
            }
            default:
                alert(`Invalid ws message kind: ${kind}`);
        }
    };

    socket.onclose = () => {
        if (attempt === 0) {
            console.log('WS connection closed, reconnecting...');
            setTimeout(() => coreConnect({attempt: 1}), 2000)
        } else {
            console.log('WS connection closed.');
        }
    };
    socket.onerror = (event) => {
        if (attempt === 0) {
            console.log(`WS connection error: ${event.text}, reconnecting`);
            setTimeout(() => coreConnect({attempt: 1}), 2000)
        } else {
            console.log(`WS reconnection failed.`);
        }

    };
}

const filesUpload = async (uploadId, file) => {
    const data = new FormData();
    data.append('file', file);
    await request(
        {
            uri: uploadMethod, method: 'POST',
            data: data, headers: {'X-Upload-Id': uploadId}
        }
    );
}

const filesList = async () => {
    const jsonData = await request({uri: listMethod});
    return jsonData['data']['items'];
}

const filesDelete = async ({key}) => {
    return await request({
            uri: deleteMethod,
            method: 'POST',
            data: {'key': key},
            is_json: true,
        }
    );
}




