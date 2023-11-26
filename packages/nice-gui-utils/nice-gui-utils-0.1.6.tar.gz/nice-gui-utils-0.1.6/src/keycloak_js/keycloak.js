export default {
    template: "<div></div>",
    mounted() {
        this.keycloak = globalKeycloakInstance;
    },
    methods: {
        initialize(initConfig) {
            this.keycloak.init(initConfig).then(
                    authenticated => {
                        if (authenticated) {
                            this.keycloak.onTokenExpired = this.keycloak.updateToken;
                        }
                    }

            );
        },
        token() {
            return this.keycloak.token;
        },
        refreshToken() {
            return this.keycloak.refreshToken;
        },
        authenticated() {
            return this.keycloak.authenticated;
        },
        login(options) {
            return this.keycloak.login(options);
        },
        logout(options) {
            return this.keycloak.logout(options);
        }
    }
};