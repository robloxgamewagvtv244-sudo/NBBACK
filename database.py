import sqlite3
class DB:
 def __init__(self,p):
  self.c=sqlite3.connect(p,check_same_thread=False)
  self.c.execute('CREATE TABLE IF NOT EXISTS settings(g INTEGER,k TEXT,v TEXT,PRIMARY KEY(g,k))')
  self.c.execute('CREATE TABLE IF NOT EXISTS xp(g INTEGER,u INTEGER,x INTEGER,t INTEGER,PRIMARY KEY(g,u))'); self.c.commit()
 def set(self,g,k,v): self.c.execute('INSERT OR REPLACE INTO settings VALUES(?,?,?)',(g,k,str(v))); self.c.commit()
 def setting(self,g,k):
  r=self.c.execute('SELECT v FROM settings WHERE g=? AND k=?',(g,k)).fetchone(); return r[0] if r else None
 def last(self,g,u):
  r=self.c.execute('SELECT t FROM xp WHERE g=? AND u=?',(g,u)).fetchone(); return r[0] if r else 0
 def xp(self,g,u,n,t):
  self.c.execute('INSERT INTO xp VALUES(?,?,?,?) ON CONFLICT(g,u) DO UPDATE SET x=x+excluded.x,t=excluded.t',(g,u,n,t)); self.c.commit()
 def total(self,g,u):
  r=self.c.execute('SELECT x FROM xp WHERE g=? AND u=?',(g,u)).fetchone(); return r[0] if r else 0
 def top(self,g): return self.c.execute('SELECT u,x FROM xp WHERE g=? ORDER BY x DESC LIMIT 10',(g,)).fetchall()
