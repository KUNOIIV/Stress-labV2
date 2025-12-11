from locust import HttpUser, task, between

class LobbyKiller(HttpUser):
    host = "http://localhost:5000"          # This points to the multiplayer_lobby.py file
    wait_time = between(0.05, 0.2)          # super aggressive

    @task
    def spam_join(self):
        # We only hit the root route (from multiplayer_lobby file)
        # The real damage comes from opening thousands of Socket.IO connections
        self.client.get("/")   # this triggers the Socket.IO handshake