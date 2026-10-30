SELECT 
    l.nome AS `Nome do Local`, 
    l.cidade AS `Cidade`, 
    r.nome AS `Recurso`, 
    r.situacao AS `Situação` 
FROM locais l
INNER JOIN recursos r ON l.id_local = r.id_local
ORDER BY l.nome;
