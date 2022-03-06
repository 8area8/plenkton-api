import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import './assets/tailwind.css';
import VueAuth0Plugin from 'vue-auth0-plugin';

// https://www.npmjs.com/package/vue-auth0-plugin
const authParams = {
    domain: 'plenkton.eu.auth0.com',
    client_id: 'nkxdOPrn8iiACVDa4jNc81FExjRpufSO',
    redirect_uri: window.location.origin
}

createApp(App).use(store).use(router).use(VueAuth0Plugin, authParams).mount('#app')
