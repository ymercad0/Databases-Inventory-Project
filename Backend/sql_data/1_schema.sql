CREATE TABLE IF NOT EXISTS warehouse (
    wid SERIAL PRIMARY KEY,
    wname VARCHAR(255) NOT NULL,
    wcountry VARCHAR(255) NOT NULL,
    wregion VARCHAR(255) NOT NULL,
    wcity VARCHAR(255) NOT NULL,
    wstreet VARCHAR(255) NOT NULL,
    wzipcode VARCHAR(255) NOT NULL,
    wbudget DOUBLE PRECISION NOT NULL,
    UNIQUE(wname, wcity)
);

CREATE TABLE IF NOT EXISTS supplier (
    sid SERIAL PRIMARY KEY,
    sname VARCHAR(255) UNIQUE NOT NULL,
    scountry VARCHAR(255) NOT NULL,
    scity VARCHAR(255) NOT NULL,
    sstreet VARCHAR(255) NOT NULL,
    szipcode VARCHAR(255) NOT NULL,
    sphone VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS racks (
    rid SERIAL PRIMARY KEY,
    rname VARCHAR(255) NOT NULL,
    rcapacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS parts (
    pid SERIAL PRIMARY KEY,
    pname VARCHAR(255) NOT NULL,
    pcolor VARCHAR(255) NOT NULL,
    pmaterial VARCHAR(255) NOT NULL,
    MSRP DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS supplies (
    sid INTEGER REFERENCES supplier(sid) NOT NULL,
    pid INTEGER REFERENCES parts(pid) NOT NULL,
    stock INTEGER NOT NULL,
    PRIMARY KEY(sid, pid)
);

CREATE TABLE IF NOT EXISTS customer(
    cid SERIAL PRIMARY KEY,
    cfname VARCHAR(255) NOT NULL,
    clname VARCHAR(255) NOT NULL,
    czipcode VARCHAR(255) NOT NULL,
    cphone VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    uid SERIAL PRIMARY KEY,
    ufname VARCHAR(255) NOT NULL,
    ulname VARCHAR(255) NOT NULL,
    username VARCHAR(255) UNIQUE NOT NULL,
    uemail VARCHAR(255) UNIQUE NOT NULL,
    upassword VARCHAR(255) NOT NULL,
    wid INTEGER REFERENCES warehouse(wid) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    tid SERIAL PRIMARY KEY,
    tdate DATE NOT NULL,
    part_amount INTEGER NOT NULL,
    pid INTEGER REFERENCES parts(pid) NOT NULL,
    uid INTEGER REFERENCES users(uid) NOT NULL,
    wid INTEGER REFERENCES warehouse(wid) NOT NULL
);

CREATE TABLE IF NOT EXISTS outgoing_transaction(
    otid SERIAL PRIMARY KEY,
    unit_sale_price DOUBLE PRECISION NOT NULL,
    cid INTEGER REFERENCES customer(cid) NOT NULL,
    tid INTEGER REFERENCES transactions(tid) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS incoming_transaction(
    itid SERIAL PRIMARY KEY,
    unit_buy_price DOUBLE PRECISION NOT NULL,
    sid INTEGER REFERENCES supplier(sid) NOT NULL,
    rid INTEGER REFERENCES racks(rid) NOT NULL,
    tid INTEGER REFERENCES transactions(tid) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS transfer(
    transferId SERIAL PRIMARY KEY,
    to_warehouse INTEGER REFERENCES warehouse(wid) NOT NULL,
    user_requester INTEGER REFERENCES users(uid) NOT NULL,
    tid INTEGER REFERENCES transactions(tid) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS stored_in(
     wid INTEGER REFERENCES warehouse(wid) NOT NULL,
     pid INTEGER REFERENCES parts(pid) NOT NULL,
     rid INTEGER REFERENCES racks(rid) NOT NULL,
     parts_qty INTEGER NOT NULL,
     UNIQUE (wid, pid),
     UNIQUE (rid),
     PRIMARY KEY (wid, pid)
);