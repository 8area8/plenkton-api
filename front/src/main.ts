import { createApp } from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import "./assets/tailwind.css";
import VueAuth0Plugin from "vue-auth0-plugin";

// https://www.npmjs.com/package/vue-auth0-plugin
const authParams = {
  domain: process.env.VUE_APP_AUTH0_ISSUER,
  audience: process.env.VUE_APP_AUTH0_AUDIENCE,
  client_id: process.env.VUE_APP_AUTH0_FRONT_ID,
  redirect_uri: window.location.origin,
};

createApp(App)
  .use(store)
  .use(router)
  .use(VueAuth0Plugin, authParams)
  .mount("#app");
