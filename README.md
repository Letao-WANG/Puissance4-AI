Puissance4-AI
==============


Deniza Alzhanova and Letao Wang


Abstract french. Puissance4 est un jeu de société très connu et nous avons implémenté plusieurs algorithmes d'IA pour ce jeu en nous basant sur les cours d'IA de semestre 6. En plus de la mise en œuvre de l'algorithme de base Minimax, élagage αβ, nous avons également mis en œuvre le MCTS (Monte Carlo tree search), qui a été testé et, avec 5000 recherches MCTS, atteint fondamentalement une solution parfaite pour chaque étape, ce qui rend très difficile pour les humains d'obtenir une victoire contre l'IA.

Méthodologie :
-----------

- Définir la structure représentant les états (données + fonctions)
- Implémenter la boucle de jeu pour 2 joueurs humains
- Implémenter l'algorithme Monte Carlo tree search
- Remplacer un joueur humain par l’ordinateur avec l'algorithme MCTS


- Implémenter et intégrer l’élagage αβ 
- Remplacer un joueur humain par l’ordinateur avec l’élagage αβ, avec plusieurs difficultés de jeu
- 3 profondeurs de recherche
- 2 fonctions d'évaluation
- Universalité de l'algorithme
