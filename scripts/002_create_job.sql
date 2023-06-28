-- Create table `job`
CREATE TABLE IF NOT EXISTS job
(
    id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    url      VARCHAR(750) UNIQUE NOT NULL,
    server_id BIGINT,
    priority INT DEFAULT 0 NOT NULL,
    done     BOOLEAN DEFAULT FALSE NOT NULL,
    success  BOOLEAN DEFAULT NULL,
    CHECK ((done AND success IS NOT NULL) OR (NOT done AND success IS NULL)),
    FOREIGN KEY (server_id) REFERENCES server(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = RocksDB;
