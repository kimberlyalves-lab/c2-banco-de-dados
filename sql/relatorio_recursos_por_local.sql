SELECT 
    situacao AS `Situação do Recurso`, 
    COUNT(1) AS `Quantidade Total` 
FROM recursos 
GROUP BY situacao;
