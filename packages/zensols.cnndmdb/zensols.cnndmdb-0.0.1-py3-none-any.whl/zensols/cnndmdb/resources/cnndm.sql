-- meta=init_sections=create_tables,create_idx

-- name=create_idx
create index article_corp_id on article(corp_id);
create index article_split on article(split);
create index article_publisher on article(publisher);
create index article_txt on article(txt);
create index highlight_article_id on highlight(article_id);
create index highlight_seq_id on highlight(seq);
create index highlight_txt on highlight(txt);


-- name=create_tables
create table article (corp_id char(40), split char(1), publisher char(1), txt text);
create table highlight (article_id int, seq int, txt text);


-- name=insert_article
insert into article(corp_id, split, publisher, txt)
    values (?, ?, substr(?, 0, 2), ?);

-- name=select_article_keys
select rowid from article;

-- name=select_article_exists_by_id
select count(*) from article where rowid = ?;

-- name=select_article_by_id
select rowid, a.*
    from article a
    where a.rowid = ?;

-- name=select_id_by_corp_id
select rowid from article where corp_id = ?;

-- name=select_article_shortest_ids
select rowid
    from article a
    order by length(a.txt)
    limit ?;


-- name=insert_highlight
insert into highlight (article_id, seq, txt) values
  ((select rowid from article where corp_id = ?), ?, ?);

-- name=select_highlight_by_id
select txt from highlight where article_id = ? order by seq;

-- name=select_highlight_by_corp_id
select h.txt
  from article a, highlight h
  where h.article_id = a.rowid and
       a.rowid = ?
  order by h.seq;
