## **Thème : comment intégrer un programme malveillant dans un logiciel sain ?** 

L'intégration de code malveillant dans un logiciel sain est une technique souvent appelée "trojanisation" ou "injection de code". Du point de vue de la sécurité informatique et de la défense des systèmes, comprendre ce mécanisme est essentiel pour analyser les menaces et concevoir des contre-mesures efficaces. Voici comment ce processus se déroule d'un point de vue technique, ainsi que les méthodes utilisées pour détecter et bloquer ces modifications. Mécanismes techniques d'injection. Les attaquants ou les analystes de logiciels malveillants (dans un cadre de test d'intrusion autorisé) utilisent généralement trois approches principales pour modifier un binaire existant : 

## 1. Modification du point d'entrée (Entry Point Hijacking) 

Principe : Les fichiers exécutables (comme les formats PE sous Windows ou ELF sous Linux) possèdent un en-tête qui indique au système d'exploitation où commence l'exécution du code (le AddressOfEntryPoint). 

Action : L'injecteur modifie cette adresse pour qu'elle pointe vers une nouvelle section contenant le code malveilant. 

Résultat : Le code malveillant s'exécute en premier, puis redirige l'exécution vers le code d'origine pour que l'utilisateur ne se doute de rien. 

2. L'injection dans les "grottes de code" (Code Caves) 

Principe : De nombreux logiciels compilés contiennent des zones de mémoire vides (remplies de zéros ou d'instructions nulles comme NOP) créées par l'alignement des sections lors de la compilation. 

Action:  Le  code  malveillant  est  inséré  directement  dans  ces  espaces vides existants. 

Résultats  :  La  taille  globale  du  fichier  ne  change  pas,  ce  qui  rend  la modification moins visible lors d'une simple inspection visuelle de la taille du fichier. 

2. Le  détournement  de  dépendances  (DLL  Hijacking  /  Shared  Object Injection) 

Principe  :  Au  lieu  de  modifier  directement  l'exécutable  principal,  cette méthode cible les bibliothèques dynamiques (fichiers .dll sous Windows ou .so sous Linux) que le logiciel charge au démarrage. 

Action :  Une  bibliothèque  malveillante  portant  le  même  nom  qu'une bibliothèque légitime est placée dans un répertoire prioritaire (souvent le même dossier que l'application). 

Résultat : L'application charge la fausse bibliothèque et exécute son code à l'insu de l'utilisateur.Méthodes de détection et de protectionLa modification non autorisée de logiciels légitimes est activement combattue par plusieurs mécanismes de sécurité standard 

Signatures numériques : Les éditeurs de logiciels sérieux signent numériquement leurs exécutables à l'aide de certificats cryptographiques. Si le moindre octet du fichier est modifié, la signature devient invalide et le système d'exploitation (comme Windows SmartScreen) bloque l’exécution. 

Contrôle  d'intégrité  (Hashing)  :  Les  solutions  de  sécurité  comparent l'empreinte cryptographique (SHA-256) du fichier en cours d'exécution avec une base de données de fichiers connus et sains. 

Analyse comportementale (EDR/Antivirus) : Même si le code malveillant est masqué au sein d'un outil d'apparence légitime, ses actions (tentatives de connexion réseau suspectes, modification du registre, injection de processus) seront  détectées  par  la  surveillance  comportementale  en  temps réel. 

Les pirates informatiques utilisent de nombreuses techniques d'attaque pour exploiter les systèmes informatiques, et ils en inventent constamment de nouvelles. Bien qu'il soit impossible de protéger votre entreprise contre toutes les  menaces  de  logiciels  malveillants,  comprendre  et  éviter  les  quatre principales méthodes utilisées par les pirates contribuera grandement à réduire votre risque d'infection. 

Les 4 principaux modes de propagation des logiciels malveillants 

Blog : 

1. Courriels d'hameçonnage 

De loin, la méthode la plus courante utilisée par les pirates informatiques et les organisations de piratage parrainées par des États pour diffuser des logiciels malveillants est l'hameçonnage. Les pirates sont devenus extrêmement habiles pour concevoir des courriels qui incitent les employés à cliquer sur des liens ou à télécharger un fichier contenant un code malveillant. Les anciens courriels d'hameçonnage, comme celui du prince nigérian qui prétend vouloir partager sa fortune avec vous (moyennant une somme modique), ont été remplacés par des courriels très convaincants qui imitent même le logo et l'identité visuelle d'une entreprise. Ces courriels d'hameçonnage se présentent sous toutes les formes,  tailles  et  couleurs,  mais  nous  souhaitons  souligner  leur  point commun : un sentiment d'urgence. 

L'un  des  indices  révélateurs  d'un  courriel  d'hameçonnage  est  l'adresse électronique de l'expéditeur. Dans la plupart des cas, l'expéditeur peut sembler légitime, comme « Microsoft-Support », mais l'adresse électronique associée est frauduleuse, par exemple  JohnDoe@MonDomainePiraté.com. Si vous recevez un courriel suspecté d'être un courriel d'hameçonnage, signalez-le à votre équipe de sécurité informatique interne afin qu'elle puisse l'analyser et le bloquer. Si vous ne disposez pas d'une telle équipe, bloquez-le dans votre filtre anti-spam, puis supprimez-le. 

## 2. Spam sur les réseaux sociaux 

Le spam sur les réseaux sociaux est une technique d'attaque relativement nouvelle pour les cybercriminels. Lorsque les utilisateurs naviguent sur les réseaux sociaux, regardent des photos ou restent en contact avec leurs amis, ils peuvent ne pas se rendre compte que la photo sur laquelle ils s'apprêtent à cliquer pourrait en réalité contenir un logiciel malveillant. Par exemple, certaines photos ou vidéos partagées sur un réseau social redirigent l'utilisateur vers une fausse page YouTube qui lui demande ensuite de télécharger et d'installer un plugin de lecteur vidéo. Une fois ce « lecteur vidéo » installé, il est toujours impossible de visionner la vidéo. Mais le criminel peut vous observer depuis votre ordinateur, avec un accès complet à votre appareil. La leçon à retenir : réfléchissez avant de cliquer ou de télécharger ! 

## 3. Protocole de bureau à distance 

C'est un cas classique. Je suis toujours surpris, lors de nos audits informatiques et évaluations des risques de cybersécurité pour de potentiels nouveaux clients, de  constater  que  beaucoup  présentent  encore  cette  énorme  vulnérabilité exposant leur système à Internet. 

Le protocole RDP (Remote Desktop Protocol) est un protocole de connexion permettant à un utilisateur de se connecter à un autre ordinateur via un réseau. Les cybercriminels utilisent désormais des outils automatisés pour analyser Internet et repérer les ordinateurs compatibles RDP. Ils tentent ensuite de deviner un nom d'utilisateur et un mot de passe pour accéder à l'ordinateur distant. 

## 4. Téléchargements furtifs à partir d'un site web compromis 

Et si je vous disais qu'il existe une méthode de cyberattaque capable d'infecter votre ordinateur avec un logiciel malveillant sans que vous n'ayez rien à faire ? Eh oui, vous n'auriez même pas besoin de cliquer sur un lien. Effrayant, n'estce pas ? Et c'est le cas. En moyenne, un site web est attaqué 58 fois par jour dans le but de l'infecter. Une fois infecté, le site commence à analyser l'ordinateur de chaque visiteur à la recherche de failles de sécurité. Ces failles peuvent provenir d'applications obsolètes, de correctifs système manquants ou de plugins de navigateur défectueux. Si une faille est découverte, elle est exploitée pour infecter l'ordinateur. 

Voici quelques exemples de la manière dont les logiciels malveillants peuvent se propager sur Internet et infecter votre système informatique. Heureusement, grâce à une gestion informatique rigoureuse , au respect des bonnes pratiques de sécurité, à une défense multicouche et à la formation des utilisateurs à la cybersécurité, une entreprise peut réduire son risque de cyberattaque . La vigilance  est  essentielle  pour  garder  une  longueur  d'avance  sur  les cybercriminels. N'hésitez pas à interroger votre prestataire informatique ou votre service informatique interne sur les mesures prises pour protéger votre entreprise contre la propagation des logiciels malveillants. 

