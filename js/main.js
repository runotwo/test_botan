"use strict";
Object.defineProperty(exports, "__esModule", {value: true});
const Insta = require("instagram-private-api");
const Bluebird = require("bluebird");
const inquirer = require("inquirer");
const grpc = require('grpc');
const ig = new Insta.IgApiClient();
let botUser;

const Proto = grpc.load('insta.proto');
const server = new grpc.Server();


ig.state.generateDevice('USERNAME');
(async () => {
    await ig.simulate.preLoginFlow();
    await Bluebird.try(async () => {
        const auth = await ig.account.login('USERNAME', 'PASSWORD');
        console.log('auth successful');
        await ig.feed.user(auth.pk);
        botUser = auth;
    }).catch(Insta.IgCheckpointError, async () => {
        await ig.challenge.auto(true); // Requesting sms-code or click "It was me" button
        const {code} = await inquirer.prompt([
            {
                type: 'input',
                name: 'code',
                message: 'Enter code',
            },
        ]);
        let challengeData = await ig.challenge.sendSecurityCode(code);
        await ig.feed.user(challengeData.logged_in_user.pk);
        botUser = challengeData.logged_in_user;
    }).catch(e => console.log('Could not resolve checkpoint:', e, e.stack));
    await (async () => await ig.simulate.postLoginFlow());
})();

server.addService(Proto.insta.InstaService.service, {
    GetProfiles: function (call, callback) {
        let usersDataResults = call.request.profiles.map(async (obj) => {
            if (obj.id === '0') {
                const user = await ig.user.searchExact(obj.username);
                obj = {
                    id: user.pk,
                    username: obj.username,
                    name: user.full_name,
                    is_private: user.is_private,
                    posts: []
                }
            }
            let posts = await ig.feed.user(obj.id);
            await Bluebird.try(async () => {
                posts = await posts.items();
            }).catch((e) => {
                posts = []
            });
            obj.posts = posts.map((post) => {
                if (post.media_type === 8) {
                    post = post.carousel_media[0]
                }
                if (post.media_type === 1) {
                    return {
                        id: post.pk,
                        type: 0,
                        link: post.image_versions2.candidates[0].url
                    }
                } else {
                    return {
                        id: post.pk,
                        type: 1,
                        link: post.video_versions[0].url
                    }
                }
            });
            return obj;
        });
        Promise.all(usersDataResults).then((data) => callback(null, data));
    }
});

server.bind('0.0.0.0:3000',
    grpc.ServerCredentials.createInsecure());
server.start();
