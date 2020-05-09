CREATE TABLE IF NOT EXISTS login(
 usuario TEXT NOT NULL,
 senha TEXT NOT NULL,
 PRIMARY KEY(usuario)
);
INSERT INTO
    login (usuario, senha)
VALUES
    ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
    ('wesley', '1056711924f951df3ead6a89e9f8d72db8c3d7353f1779a7abb33ed28802e46b'),
    ('denis', '7619ee8cea49187f309616e30ecf54be072259b43760f1f550a644945d5572f2');