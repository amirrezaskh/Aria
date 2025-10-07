::: IEEEkeywords
Split Learning, SplitFed Learning, Sharding, Blockchain, Federated
Learning, Scalability, Security.
:::

# Introduction

Data privacy is a critical concern in training machine learning models,
especially as sensitive data becomes increasingly distributed across
decentralized devices. This has led to growing interest in collaborative
learning approaches [@duan2022combined], where multiple participants
contribute to training a global model while retaining their data
locally. By sharing model updates instead of raw data, collaborative
learning significantly mitigates privacy risks.

The most widely adopted collaborative learning techniques are Federated
Learning (FL) [@mcmahan2017communication] and Split Learning (SL)
[@gupta2018distributed; @vepakomma2018split]. In FL, clients train a
global model in parallel using their local datasets and share model
updates, which are then aggregated by a server using methods like FedAvg
[@ZHANG2021106775]. However, FL imposes substantial computational
demands on clients, limiting its feasibility for resource-constrained
devices [@Batool2022BlockFeST]. To address this, SL introduces a
model-splitting approach, dividing the global model into smaller
client-side and larger server-side segments. Clients train the smaller
segment with fewer layers, while the server handles the larger segment,
thereby reducing computational overhead on clients. Despite this
advantage, SL suffers from prolonged training times due to sequential
client-server interactions and frequent communication for each batch
[@duan2022combined; @Gao2020endtoend; @ceballos2020splitnn]. Moreover,
SL achieves lower efficiency compared to FL, as it does not fully
exploit aggregation techniques like FedAvg [@thapa2022splitfed].

To tackle these challenges, SplitFed Learning (SFL) [@thapa2022splitfed]
was introduced as a hybrid approach that combines the strengths of FL
and SL. SFL incorporates an additional federated server to aggregate
client-side updates using the FedAvg algorithm, significantly reducing
the training time compared to SL. However, as the number of clients
increases, the computational burden on the SL server becomes
substantial. Additionally, the growing number of clients exacerbates
communication overhead, placing a strain on the network infrastructure.

The scalability limitations of both SL and SFL extend beyond
infrastructure concerns to performance degradation. As highlighted in
[@oh2022locfedmix; @pal2021server; @oh2023mix2sfl], an imbalance in
model updates between the SL server and clients leads to a decline in
model performance as the client count increases.

SFL architectures also face severe security challenges. For instance, a
malicious FL server could compromise the integrity of the global model
by selectively including harmful updates [@li2021bflc]. Similarly,
malicious clients may disrupt the system by submitting corrupted
updates. Moreover, the centralized nature of both servers creates single
points of failure, posing significant operational risks as the servers
holds all contributions to the global model [@qu2022blockchain].

To overcome these challenges, we introduce the first end-to-end
decentralized and scalable blockchain-enabled SplitFed Learning
architecture. We begin our design by first proposing Sharded SplitFed
Learning (SSFL), a novel architecture designed to enhance the
scalability and performance of SFL by distributing the SL server
workload across multiple parallel shards. In SSFL, clients are assigned
to separate shards, effectively balancing the computational load and
improving training efficiency. SSFL also addresses the issue of
imbalanced model updates in SFL by employing an additional federated
server that aggregates the shard-level models using the FedAvg algorithm
[@mcmahan2017communication]. This aggregation effectively "smooths out\"
each SL server's model updates, mitigating the adverse effects of high
local learning rates and server biases that can impede convergence. By
leveraging this approach, SSFL not only improves scalability but also
enhances the stability and convergence speed of SFL.

Furthermore, we expand our design by integrating the blockchain
architecture with SSFL to resolve persistent security vulnerabilities
due to the inherent centralization[@pasquini2021unleashing]. In this
paper, we propose Blockchain-enabled SplitFed Learning (BSFL), the first
decentralized SplitFed Learning architecture that eliminates reliance on
a central FL server and fortifies security through a committee-based
blockchain consensus mechanism [@li2021bflc]. In BSFL, tasks
traditionally handled by the central FL server---such as model
aggregation, update validation, and reward distribution---are
autonomously executed using smart contracts on the blockchain. A
decentralized committee of nodes evaluates model updates from each SFL
shard, mitigating data poisoning attacks and ensuring the integrity of
contributions. This blockchain-based framework creates a trustless,
tamper-resistant learning environment, leveraging consensus to reinforce
security, fairness, and accountability. To summarize, the contributions
of this paper are as follows:

1.  Sharded SplitFed Learning (SSFL): We propose SSFL as an enhancement
    to the existing SplitFed Learning (SFL) model to overcome its
    scalability limitations. This approach reduces computational strain
    on the SL server by enabling parallel training from multiple SFL
    shards, thus significantly improving the scalability and efficiency
    of the model. SSFL also addresses the issue of imbalanced model
    updates by reducing the effective learning rate through federated
    averaging. SSFL is particularly beneficial in environments with a
    large number of resource-constrained devices.

2.  Blockchain-enabled SplitFed Learning (BSFL): We introduce BSFL, the
    first blockchain-enabled SFL framework, to address the
    centralization-related security vulnerabilities in SFL. BSFL
    replaces the centralized FL server with a blockchain architecture
    employing a committee-based consensus mechanism. It incorporates an
    evaluation process to assess client model updates, thereby
    mitigating risks such as data poisoning and model tampering while
    enhancing system fairness, robustness, and performance.

3.  Experiments and Evaluation: We demonstrate the effectiveness of SSFL
    and BSFL through comprehensive experiments designed to measure
    performance under both standard operating conditions and simulated
    data-poisoning attacks. Additionally, we compare the round
    completion time and convergence speed of our approaches with
    traditional SL and SFL models, demonstrating superior performance
    and operational efficiency.

The remainder of this paper is organized as follows. In Section
[2](#sec:related-works){reference-type="ref"
reference="sec:related-works"}, we discuss previous studies related to
scalable split learning and blockchain-enabled distributed learning.
Section [3](#sec:def){reference-type="ref" reference="sec:def"}
introduces definitions used throughout the paper. In Sections
[4](#sec:ssfl){reference-type="ref" reference="sec:ssfl"} and
[5](#sec:bsfl){reference-type="ref" reference="sec:bsfl"}, we introduce
SSFL and BSFL, respectively. Section
[6](#sec:discussions){reference-type="ref" reference="sec:discussions"}
provides detailed discussions for our proposed frameworks. Section
[7](#sec:experiments){reference-type="ref" reference="sec:experiments"}
presents our comprehensive evaluation and results. At last, Sections
[\[sec:future-works\]](#sec:future-works){reference-type="ref"
reference="sec:future-works"} and
[9](#sec:conclusion){reference-type="ref" reference="sec:conclusion"}
address the future works and conclusion.

# Related Works {#sec:related-works}

FL was first proposed by McMahan et al. [@mcmahan2017communication] to
enhance the privacy of data holders in machine learning training
procedures. In FL, a network comprising clients containing local
datasets and a server capable of communicating with all clients is
established. In this scenario, clients contribute to training a selected
global model by sharing model updates instead of their sensitive data to
preserve their right to privacy [@kairouz2021advances]. In FL, clients
train a global model using their local datasets, which requires
substantial computational resources. To address this limitation, Gupta
and Raskar [@gupta2018distributed] introduced SL. In SL, the machine
learning model is divided into smaller segments: clients train the
smaller segments locally, while the server performs the heavier
computational tasks. However, SL involves significant communication
overhead between clients and the server, requiring two messages per
batch for each client. Consequently, the convergence time of SL is much
slower compared to FL.

SFL is introduced by Thapa et al. [@thapa2022splitfed] as a new
collaborative and distributed learning framework that combines the
strengths of FL and SL to overcome the limitations of both approaches.
SFL operates as a variation of SL, where clients train their model
segments and communicate with the server in parallel. Additionally,
client model updates are aggregated using the FedAvg algorithm by a
federated server. By integrating FL into the SL architecture, SFL
significantly improves the speed and efficiency of the original SL
framework.

## Scalibility

The inherent model split nature of SL and SFL has been identified as a
key factor limiting their scalability [@oh2022locfedmix]. In parallel
SL, the server model segment is updated significantly more often than
the client segments, resulting in an uneven learning rate between the
two. This imbalance can lead to inefficient training, especially when
client model updates are handled separately from the server model. To
address these challenges, LocFedMix-SL was introduced, incorporating
local regularization of client models and augmenting clients' smashed
data to improve server model training [@oh2022locfedmix]. Building on
this work, additional solutions have been proposed. For instance, Pal et
al. [@pal2021server] addressed the same issues by implementing different
learning rates for the server and clients, along with broadcasting
similar gradients to all clients. Later, Mix2SFL combined these
approaches to achieve optimized performance, ensuring both enhanced
accuracy and improved communication efficiency [@oh2023mix2sfl].
Although these methods effectively tackle performance issues related to
scalability, they fall short in addressing the computational and
communication overhead of the server and its impact on overall
efficiency. To bridge this gap, we propose SSFL, a novel sharding
approach designed to enhance the accuracy, stability, and scalability of
SFL.

## Security

The intersection of blockchain technology and FL has emerged as a
promising avenue for addressing persistent challenges in secure and
privacy-preserving machine learning. FL enhances data privacy by
facilitating distributed training and aggregating model updates instead
of collecting private datasets. However, despite its privacy-preserving
design, security vulnerabilities persist in the FL architecture
[@lyu2020threats]. One major concern arises from malicious clients, who
may intentionally transmit harmful model updates to degrade the
performance of the global model. Similarly, the centralized server in FL
introduces risks of unfairness, as it may selectively aggregate specific
model updates, potentially biasing the global model. Moreover, the
server is susceptible to performing Membership Inference Attacks (MIA)
[@shokri2017membership] on the received model updates, enabling it to
infer details about clients' local datasets. Although employing
differential privacy [@dwork2006differential] mitigate the risk of MIAs,
this approach often comes at the cost of reduced model performance and
efficiency [@li2020fl]. As a result, addressing these security
challenges without compromising the effectiveness of FL remains an open
area of research, prompting the exploration of blockchain as a potential
solution.

To resolve these issues, blockchain-enabled federated learning
approaches were suggested [@qu2022blockchain]. The decentralized feature
of blockchains eliminate the challenges related to the server component
in FL. In addition, the inherent incentive mechanisms utilized by
blockchains contribute to encouraging local clients to train truthfully
and communicate honest model updates to receive greater rewards. Kim et
al. [@kim2020blockfl] introduced the first blockchain-enabled federated
learning framework called BlockFL. Following their proposal, Li et al.
[@li2021bflc] introduced a blockchain-based FL blueprint utilizing a
committee consensus. The committee consensus used in our design is
motivated by this study. A similar committee consensus has also been
incorporated in Proof-of-Collaborative-Learning [@Sokhankhosh2024PoCL],
which leverages blockchain computation power to distributedly train FL
models. The integration of blockchain with FL extends beyond committee
consensus mechanisms and includes various enhancements, such as its
combination with differential privacy
[@truex2019hybrid; @qu2021proof; @Lu2020PoTQ], Layer 2 (L2) solutions
[@Yuan2021ChainsFL; @Alief2023FLB2], and Zero-Knowledge Proofs (ZKPs)
[@zhang2023blockchain]. These approaches collectively aim to enhance
privacy, scalability, and security in blockchain-enabled FL frameworks.

The integration of blockchain networks with SL remains relatively
underexplored. BlockFeST, proposed by Batool et al.
[@Batool2022BlockFeST], combines blockchain with federated and split
learning, offloading major computational responsibilities to an SL
server to alleviate the computational burden on FL clients. Similarly,
Sai [@Sai2024Ablockchain] introduced a blockchain-enabled split learning
framework that leverages smart contracts to dynamically select servers
and clients for each training round.

![Overview of Sharding SplitFed Learning
framework.](Images/ssfl.png){#fig:ssfl width="\\linewidth"}

While both approaches improve fairness and security, they continue to
face significant challenges related to centralization and scalability.
Hence, to the best of our knowledge, we are the first to propose
Blockchain-enabled SplitFed Learning to eradicate the security,
fairness, and performance concerns of Split Learning.

# Definitions {#sec:def}

To enhance the readability of the paper, let us define a few
incorporated terms of our design.

**Client**: A client is any node in a decentralized learning algorithm
that possesses private data and contributes to the training process by
training a model locally on its dataset.

**Server**: A server is any node that participates in distributed
training without holding private data. In Split Learning (SL), the
server trains the computationally intensive portion of the model. In
Federated Learning (FL), the server solely aggregates client models to
construct a new global model. Since the SFL, SSFL, and BSFL algorithms
include both Split Learning and Federated Learning servers, their
distinction is vital for understanding the algorithms presented in the
paper.

**Node**: A node refers to any participant in the training process,
either a client or a server (SL or FL).

# Sharded SplitFed Learning {#sec:ssfl}

As a variation of SL, SFL combines the beneficial characteristics of
both SL and FL to address their respective limitations. In the SFL
architecture, two primary innovations are introduced: parallel client
training and a federated server that aggregates client models at each
training round. While these modifications significantly reduce SL's
convergence time, scalability remains a major challenge. In both SFL and
SL, as the number of clients increases, the computational and
communication overhead on the central SL server grows substantially,
limiting the feasibility of these architectures in large-scale,
real-world applications.

:::: algorithm
::: algorithmic
[]{#alg:ssfl label="alg:ssfl"} _/\* Executes on each Shard Server (SFL
Server) \*/_ **TrainingCycle**($c$):
$(A_{j,r}, Y_{j,r}) \leftarrow \text{ClientTrain}(W^C_{j,r})$
$\hat{Y}_{j,r} \leftarrow \text{ServerForwardPass}(A_{j,r}, W^S_{i,j,r})$
$\mathcal{L}_{j,r} \leftarrow \text{Loss}(Y_{j,r}, \hat{Y}_{j,r})$
$\nabla \ell_j(W^S_{i,j,r}, A_{j,r}) \leftarrow \text{ComputeGradients}(\mathcal{L}_{j,r})$
$W^S_{i,j,r} \leftarrow W^S_{i,j,r} - \lambda \cdot \nabla \ell_j(W^S_{i,j,r})$
Send $d A_{j,r} := \nabla \ell_j(W^S_{i,j,r}, A_{j,r})$ to client $j$.
Update shard server model:
$W^S_{i,r+1} \leftarrow \frac{1}{J} \sum_{j=1}^{J} W^S_{i,j,r}$ _/\*
Executes on the Federated Learning (FL) Server \*/_ **Training**(): Call
**TrainingCycle**($t$) for shard $i$. _/\* Executes on the Federated
Learning (FL) Server \*/_ **Aggregate**(): Receive $W^S_{i,t}$ and
$W^C_{j,t}$ updates from each shard server $i$ and client $j$. Update
global models:
$W^S_{t+1} \leftarrow \frac{1}{I} \sum_{i=1}^{I} W^S_{i,t}$
$W^C_{t+1} \leftarrow \frac{1}{J} \sum_{j=1}^{J} W^C_{j,t}$
:::
::::

However, the scalability challenges in SL and SFL are not solely limited
by infrastructure capacity. SL and its variations experience a
performance degradation that intensifies as the number of clients
increases. In these frameworks, the server-side model is updated far
more frequently than the client-side model on each local device,
resulting in an imbalance in model training. Consequently, as the client
count grows, this disparity between server and client models leads to a
substantial decline in overall performance. While previous studies have
proposed various solutions to address the performance and efficiency
limitations of SL and SFL in scalable environments
[@oh2022locfedmix; @pal2021server; @oh2023mix2sfl], to the best of our
knowledge, no work has comprehensively addressed the imbalanced training
problem, as well as the challenges of server-side computation and
communication overhead.

To tackle these challenges, we propose Sharded SplitFed Learning (SSFL),
an enhanced framework where clients are organized across multiple shard
servers, each acting as a conventional SplitFed Learning SL server. The
SSFL architecture, illustrated in Figure
[1](#fig:ssfl){reference-type="ref" reference="fig:ssfl"}, introduces an
additional federated server that aggregates model updates from all shard
servers in parallel. Although we depict the two FL servers as separate
entities, their responsibilities can be handled by a single instance if
the framework implements specific security measures, such as encrypted
model updates for clients and servers. For simplicity in our
explanation, we assume that these precautions are taken, and the system
is only comprised of one FL server aggregating both client and SL server
models of the SplitFed Learning networks.

## SSFL Workflow

To start training, clients join an SFL network within the system by
sending a handshake request to one of the available SFL servers. Upon
joining, clients begin training by performing a forward pass on the
global client model using their local data. Each batch's output and
target are sent to the designated SFL server to continue training.
Servers then conduct a forward pass on the received outputs, progressing
through the split layer until reaching the final layer, where they
compute gradients and update the local SFL server model. The gradient of
the final layer is also sent back to the clients, enabling clients to
update their respective models. Once all shards complete their local
training and aggregation, both clients and SFL servers send their
updated models to the FL server for a final aggregation step. Each FL
aggregation completes a **cycle** of training in SSFL. To formalize the
SSFL training process, we present Algorithms
[\[alg:ssfl\]](#alg:ssfl){reference-type="ref" reference="alg:ssfl"} and
[\[alg:clients\]](#alg:clients){reference-type="ref"
reference="alg:clients"}, which detail each workflow component in
sequence. Table
[\[table:notation\]](#table:notation){reference-type="ref"
reference="table:notation"} is an accompanying notation table that
provides clear definitions of the variables, parameters, and functions
utilized within these algorithms, serving as a reference to streamline
understanding.

## Scalability and Performance

:::: algorithm
::: algorithmic
[]{#alg:clients label="alg:clients"} _/\* Executes on each client device
\*/_ **ClientTrain**():
$A_{j,r} \leftarrow \text{ClientForwardPass}(X_j, W^C_{j,r})$ Assuming
$Y_j$ is the label of $X_j$ Send $(A_{j,r}, Y_{j})$ to the assigned
shard server _/\* Executes on each client after receiving the gradients
\*/_ **ClientBackProp**(): Receive $d A_{j,r}$ from shard server.
$\nabla \ell_j(W^C_{j,r}) \leftarrow \text{BackPropagate}(d A_{j,r})$
$W^C_{j,r} \leftarrow W^C_{j,r} - \lambda \cdot \nabla \ell_j(W^C_{j,r})$
:::
::::

Incorporating shards into the SFL network significantly reduces the
computational load on individual SFL servers by distributing the forward
and backward propagation tasks across multiple servers. This sharding
approach not only enhances scalability by effectively expanding the
system's infrastructure capacity but also improves performance under
increasing client numbers. In addition, the sharding mechanism addresses
the performance-level scalability challenge, which arises due to the
imbalance in learning rates between the SFL server and client models.

As discussed by [@oh2022locfedmix], this performance issue stems from
the SFL server's effective learning rate being higher than that of the
clients, leading to disproportionately faster updates in the SFL server
model compared to client models. This discrepancy results in unstable
and suboptimal training as the number of clients increases. To address
this imbalance, studies like LocFedMix [@oh2022locfedmix] and SGLR
[@pal2021server] propose solutions such as augmenting smashed client
data or adjusting the learning rate to align client and server updates
better.

Instead, in our approach, we propose introducing an additional federated
server to aggregate updates from shard SFL servers. By using this extra
FL server layer, we reduce the learning rate of the shard servers,
creating a more balanced and synchronized training process. This
adjustment not only mitigates the risk of performance degradation but
also ensures that both SFL server and client models progress at a
harmonious rate, thereby enhancing the overall stability and efficiency
of the training framework.

:::: algorithm
::: algorithmic
_/\* Runs on each SFL server /_ **TrainingCycle**($c$):
$(A_{j,r}, Y_{j,r}) \leftarrow \text{ClientTrain}(W^C_{j,r})$
$\hat{Y}_{j,r} \leftarrow \text{ServerForwardPass}(A_{j,r}, W^S_{i,j,r})$
$\mathcal{L}_{j,r} \leftarrow \text{Loss}(Y_{j,r}, \hat{Y}_{j,r})$
$\nabla \ell_j(W^S_{i,j,r}, A_{j,r}) \leftarrow \text{ComputeGradients}(\mathcal{L}_{j,r})$
Send $d A_{j,r} := \nabla \ell_j(W^S_{i,j,r}, A_{j,r})$ to each client
$j$. Update shard server model:
$W^S_{i,r+1} \leftarrow \frac{1}{J} \sum_{j=1}^{J} W^S_{i,j,r}$ Send
$W^S_{i,R}$ to blockchain ledger. Request each client
$j \in \text{shard}$ to submit $W^C_{j,R}$ to ledger. _/\* Runs on each
SFL server \*/_ **Evaluate**($W^S_{i,R}$, \[$W^C_{j,R}$ for each client
$j$\]): Initialize **scores** as an empty list.
$A_{j,R} \leftarrow \text{ClientForwardPass}(X, W^C_{j,R})$
$\hat{Y}_{j,R} \leftarrow \text{ServerForwardPass}(A_{j,R}, W^S_{i,R})$
$\mathcal{L}_{j,R} \leftarrow \text{Loss}(Y_{j,R}, \hat{Y}_{j,R})$
Append $\mathcal{L}_{j,R}$ (validation loss) to **scores**.
**Median**(**scores**) _/\* Runs on the blockchain network \*/_
**Committee Procedure**: Randomly select committee members. Select
committee members based on scores from the previous cycle.
**TrainingCycle**($t$) Receive all $W^S_{i,R}$ and $[W^C_{j,R}]$
updates. Send $W^S_{i,R}$ and $[W^C_{j,R}]$ to other committee members.
Call **Evaluate** to obtain validation scores. Assign the median of all
scores given to shard $i$ as the final score. Sort scores and select top
$k$ model updates. Update global models:
$W^S_{t+1} \leftarrow \frac{1}{K} \sum_{k=1}^{K} W^S_{k,t}$
$W^C_{t+1} \leftarrow \frac{1}{K \cdot J} \sum_{k=1}^{K} \sum_{j=1}^{J} W^C_{k,j,t}$
:::
::::

# Blockchain-enabled SplitFed Learning {#sec:bsfl}

While sharding enhances both the performance and scalability of the SSFL
framework, centralization at the server side still introduces several
security and reliability risks: (i) The FL server may exhibit bias by
favouring certain clients, either intentionally or due to external
manipulation, which can alter the training loop, undermining both model
integrity and overall training efficiency. (ii) The central FL server in
SSFL and its parent systems handles all core functionalities and bears
the main workload, making it a critical single point of failure. Any FL
server failure would not only halt the system's operation but also risk
the loss or corruption of all contributions, severely impacting system
reliability and continuity. (iii) Malicious clients within the SSFL
framework may engage in data poisoning attacks, submitting manipulated
data to compromise the quality, reliability, and generalizability of the
global model. (iv) Centralization increases the risk of privacy
breaches, as the FL server handles sensitive information from all
clients. A breach or malicious access to the central FL server could
expose client data, violating privacy and confidentiality requirements.
(v) The framework assumes the central FL server is trustworthy and
operates without malice. However, if the server is compromised or
behaves maliciously, such as through collusion with external entities,
it could jeopardize the system's security, fairness, and
trustworthiness.

To address these issues, we propose decentralizing the SSFL framework
through the blockchain technology to eliminate the centralized FL server
and its associated security risks. In Blockchain-enabled SplitFed
Learning (BSFL), smart contracts on the blockchain assume the central
server's functionalities, enabling end-to-end decentralization. This
paper introduces a committee consensus mechanism within the BSFL
framework, responsible for block creation as well as the evaluation and
validation of model updates, to ensure secure, unbiased, and robust
operations. By designing SSFL and decentralizing it using BSFL, we
introduce the first Blockchain-enabled SplitFed Learning system,
enhancing fairness, efficiency, and scalability of the original SFL
algorithm.

To decentralize the tasks of FL servers, we initialize the global client
and SFL server models directly on the blockchain. This setup allows SFL
servers and clients to access the global models and commence training.
After certain SplitFed training rounds, each client and SFL server saves
their updated models on the blockchain, which subsequently triggers an
aggregate smart contract to combine these updates into a new global
model.

## Committee Consensus Mechanism

Consensus mechanisms in blockchains determine the content of blocks and
their order within the chain. In this paper, we employ a committee
consensus mechanism to evaluate model updates proposed by each shard,
selecting only the top-performing models for aggregation. In BSFL, the
SFL servers in each shard form a committee that validates each other's
model updates by assigning a score to each update during each training
cycle. By limiting communication to the committee nodes, the system
significantly reduces communication overhead. The scores assigned to
committee members are then ranked, and only the top $K$ models are
aggregated to create the updated global models. At the start of each new
cycle, a new committee is selected based on the scores from the previous
cycle, ensuring that prior committee members do not serve consecutively,
therefore reducing the risk of collusion or malicious actions.

Each committee member validates the model updates proposed by others by
evaluating their data against the newly trained models. The validation
loss, or accuracy if preferred, is reported as the score assigned by one
member to another. The final score for each committee member in that
cycle is determined by selecting the median of all scores received.

The evaluation metric can be based on either validation loss or
validation accuracy, depending on the task. The primary distinction lies
in the optimization goal: minimizing validation loss versus maximizing
validation accuracy. Additionally, it is important to note that
validation accuracy can only be utilized in classification problems,
whereas validation loss can be employed across a broader range of tasks,
including non-classification problems.

## BSFL Workflow

BSFL supervises the training procedure by utilizing three distinct smart
contracts to perform the tasks of the central FL server. In the initial
round, the _AssignNodes_ smart contract randomly selects nodes in the
system to represent the SFL servers within each shard. Subsequently,
each server is randomly assigned a set of clients to establish the
composition of each shard. The training procedure in each SFL network
follows the traditional SFL algorithm; however, upon completion, the
models are stored on the blockchain. The _ModelPropose_ smart contract
collects and distributes all trained models to each committee member,
i.e., each SFL server. The SFL servers then validate the newly trained
global models using their local data and report the validation loss as
the score for the models of other members. The median of all scores
assigned to a member's model is selected as the final score. The
_EvaluationPropose_ smart contract sorts these scores and identifies the
top $K$ models as the winners of the current cycle, with the aggregate
of these models forming the new global models for the subsequent cycle.
Algorithm [\[alg:bsfl\]](#alg:bsfl){reference-type="ref"
reference="alg:bsfl"} and
[\[alg:clients\]](#alg:clients){reference-type="ref"
reference="alg:clients"} illustrate the BSFL workflow.

## Node Assignment

The committee for each new cycle is selected based on the scores of
nodes from the previous round. To ensure fairness and enhance security,
any committee member from round $t$ is not allowed to remain on the
committee in round $t+1$. Thus, we designate a node as an SFL server if
its score surpasses those of other nodes not already chosen as servers
in the previous round. Shard nodes are assigned sequentially: an SFL
server and its clients are first allocated for one shard, followed by
the next. Since committee members from the previous cycle must take on
client roles in the current cycle, we only consider these previous
committee members when assigning clients.

The algorithm for assigning nodes as clients and SFL servers may vary
from our proposed method. Our approach groups nodes with similar
efficiency within the same shard, ensuring that even in the case of
data-poisoning attacks, the performance of honest nodes is less likely
to be overshadowed

# Discussions {#sec:discussions}

## Efficiency

The BSFL architecture enhances efficiency by selecting only the
top-performing models for aggregation, resulting in a more optimized
global model compared to SSFL. Additionally, the dynamic rotation of
committee members ensures that the global model is trained on all local
datasets in the system over time, effectively implementing a form of
distributed k-fold cross-validation.

## Security and Stability

Replacing the centralized FL server with a blockchain network enhances
the system's reliability by eliminating the central FL server as a
single point of failure. In this blockchain-based setup, all operations
are carried out using smart contracts and collectively verified by a
committee. This decentralized validation ensures secure and
uninterrupted training processes, mitigating risks commonly associated
with centralized FL servers.

## Non-IID Data

A common challenge in distributed learning is handling Non-Independent
and Identically Distributed (Non-IID) local datasets. In simpler terms,
each device might have biased or unbalanced data, for example, one
device might predominantly store cat images, while another contains
mostly dog images, resulting in local datasets that do not represent the
overall data distribution.

To counter this challenge, our framework uses data from committee
members for validation, exposing the global model to a broader, more
varied set of data during evaluation. This cross-validation reduces the
risk of overfitting by ensuring that the model is not overly specialized
to the narrow distributions of individual nodes. By validating updates
across diverse committee datasets, the system creates a more robust and
generalized global model capable of handling diverse non-IID data
effectively.

![Performance comparison for 9 nodes in 60 training
rounds.](Images/all_9.png){#fig:all_9 width="\\linewidth"}

![Performance comparison for 36 nodes in 30 training
rounds.](Images/all_36.png){#fig:all_36 width="\\linewidth"}

## Committee Election

In BSFL, we propose selecting committee members based on clients' scores
from the previous round. Alternatively, a random selection approach
could be employed to enhance model generalization by exposing the global
model to a wider variety of datasets across multiple cycles.

Our current approach optimizes performance, stability, and fairness by
selecting committee members from all clients in the previous round.
However, this approach may appear to conflict with split learning's goal
of reducing the computational burden on resource-constrained clients. To
resolve this, a more advanced committee selection algorithm could
account for nodes' computational capabilities. Restricting committee
membership to nodes capable of performing shard server duties ensures
that only suitable nodes are chosen. This refinement upholds the
integrity of split learning while ensuring fairness and efficiency.

::: table\*
:::

## Malicious Nodes

In SSFL, malicious nodes undermine system performance depending on their
roles. When acting as clients, they may submit harmful model updates to
degrade the global model's accuracy. As FL servers, they can introduce
noise into the global model or selectively favour specific clients,
reducing model generalization. To mitigate these threats, we propose
integrating a blockchain network with a committee consensus mechanism,
eliminating the central FL server while implementing an evaluation
framework for model updates. Below, we analyze the resilience of BSFL
against malicious nodes in two key scenarios:

1.  Malicious Clients: Malicious nodes may submit "poisonous\" updates
    to degrade global model performance. Our proposed evaluation and
    committee selection algorithm mitigates such attacks by discarding
    harmful submissions and retaining only the top $K$ most trustworthy
    model updates. As long as there are at least $K \times C$ honest
    clients in the system (where $C$ represents the number of clients
    per shard), the framework can maintain effective training and resist
    significant disruption from data-poisoning attacks.

2.  Malicious Committee Members: Malicious nodes may infiltrate the
    committee and attempt to undermine the evaluation process. In a
    committee of $N$ nodes, each model update receives a score from the
    remaining $N - 1$ committee members, with the final score calculated
    as the median via a smart contract. Malicious members may attempt to
    skew results by favoring inferior updates, but their impact is
    negligible unless they form a majority. To ensure resilience, BSFL
    framework requires at least $\lfloor \frac{N}{2} \rfloor + 1$
    committee members to uphold evaluation integrity. Furthermore, to
    prevent the aggregation of harmful model updates, the number of
    selected models, $K$, must remain less than $\frac{N}{2}$.

In summary, ensuring robust security in BSFL requires
$\lfloor \frac{N}{2} \rfloor + 1$ honest committee members, at least
$K \times C$ honest clients, and selecting $K$ values such that
$2 < K < \frac{N}{2}$. However, the security requirements of BSFL are
adaptable: in scenarios with minimal malicious activity, the value of
$K$ can be adjusted to prioritize efficiency over stringent security
constraints.

# Experiments {#sec:experiments}

## Settings and Normal Training

To evaluate the performance of SSFL and BSFL, we implemented both
frameworks using the Fashion MNIST dataset, which consists of 60,000
images across 10 distinct classes[^1]. We define a node as any entity,
client or SFL server, participating in a distributed learning procedure.
This distinction is necessary since the clients and SFL servers are not
static in frameworks such as BSFL. In our work, the experiments are
conducted in two different settings: one with 9 nodes and the other with
36 nodes, to assess the effectiveness of our proposed solutions in both
small-scale and large-scale scenarios. The local datasets for each node
contain an equal number of images (6,666), but they are non-IID.

![Round completion times for 36
nodes.](Images/times.png){#fig:transmission width="\\linewidth"}

Additionally, we utilized the Hyperledger Fabric blockchain framework to
implement the smart contracts (chaincodes) described in the BSFL
architecture. The nodes in our framework are built by integrating
PyTorch as the machine learning tool and Flask as the communication
interface between the nodes and the blockchain network. Each node is
implemented as a separate process in our experimental setup, which runs
on an Intel Xeon(R) 4216 CPU with 16 cores and 32 threads (2 threads per
core), along with an NVIDIA GeForce RTX 3080 GPU for accelerated
training.

We compare the effectiveness of both SSFL and BSFL by conducting
experiments under the same settings with SFL and SL. In each experiment,
we train the global models, as described in Table
[\[table:model\]](#table:model){reference-type="ref"
reference="table:model"}, to classify Fashion MNIST images. In addition,
the hyperparameters for these settings are fixed across all setups to
ensure a precise evaluation of all approaches.

In the SL and SFL setups, one of the nodes (1 out of 9 or 1 out of 36)
serves as the central server to oversee the training process. In SSFL
and BSFL, we introduce three shards, each with two clients, for
experiments involving nine nodes. When the number of nodes increases to
36, we adjust the configuration to six shards, each containing five
clients. The value of $K$, which determines the number of top-performing
shard SFL servers participating in the global model aggregation, is set
to two and three for the 9-node and 36-node scenarios, respectively.

To prevent overfitting, we employ early stopping across all approaches.
This is straightforward to implement in SSFL, SFL, and SL, as they
involve a central node that supervises the training process. For BSFL,
early stopping is achieved through the committee consensus mechanism,
which halts training when the validation loss begins to deteriorate.

Figures [2](#fig:all_9){reference-type="ref" reference="fig:all_9"} and
[3](#fig:all_36){reference-type="ref" reference="fig:all_36"} show the
validation loss of SL, SFL, SSFL, and BSFL across all training rounds.
As evident in both figures, SSFL and BSFL outperform the earlier
approaches, primarily due to the sharding mechanism employed in these
frameworks. In both frameworks, the sharded architecture eradicates the
imbalanced learning rate of split learning by aggregating the SFL server
models, enhancing global model performance. Furthermore, BSFL
demonstrates superior performance compared to SSFL by utilizing its
committee consensus evaluation, which ensures that only the
top-performing model updates contribute to the global model. Notably,
BSFL requires fewer training rounds, as its enhanced performance leads
the global model to reach optimal accuracy and begin overfitting the
training data more quickly. Finally, Table
[\[tab:performance_comparison\]](#tab:performance_comparison){reference-type="ref"
reference="tab:performance_comparison"} compares the final test loss of
all distributed learning algorithms. As shown, SSFL substantially
enhances scalability and performance over SL and SFL due to its lower
round time and test loss. Nevertheless, the test loss in the attacked
settings proves SSFL's inability to tolerate data-poisoning threats.

## Under Malicious Attacks

In our experiments, we assume that malicious nodes carry out data
poisoning attacks by sending harmful updates to the central FL server,
thereby undermining the performance of the global model. We conduct
these attacks across all approaches to validate the effectiveness of our
proposed solution. To evaluate the impact of data poisoning attacks, we
test with varying proportions of malicious nodes, specifically $33\%$
and $47\%$ for the 9-node and 36-node setups, respectively. These varied
attacker proportions allow us to evaluate the resilience and performance
of our proposed frameworks under different threat levels. Notably, the
36-node experiment with $47\%$ attackers represents a scenario where the
system is pushed to its limits, simulating the maximum number of
attackers possible without breaching the $51\%$ threshold typically
required for a successful blockchain takeover.

In BSFL, we further simulate a voting attack to assess the resilience of
the committee consensus mechanism. In this scenario, malicious nodes,
when selected as committee members, deliberately vote for the
worst-performing model updates to disrupt the aggregation process. By
examining the system's ability to counter this disruption, we evaluate
whether BSFL can still effectively aggregate the most beneficial model
updates.

Figures [2](#fig:all_9){reference-type="ref" reference="fig:all_9"} and
[3](#fig:all_36){reference-type="ref" reference="fig:all_36"} illustrate
the performance of each algorithm under identical data-poisoning
attacks. As shown in these figures, all algorithms except BSFL are
adversely impacted by these attacks, lacking effective mechanisms to
counteract them. In SL, SFL, and SSFL, data-poisoning attacks cause a
substantial increase in validation loss and decline in the global
model's performance. BSFL, however, remains entirely unaffected due to
its robust committee consensus mechanism, which effectively filters out
malicious updates from adversarial nodes. The effectiveness of BSFL in
mitigating data-poisoning attacks is also demonstrated by the test loss
values presented in Table
[\[tab:performance_comparison\]](#tab:performance_comparison){reference-type="ref"
reference="tab:performance_comparison"}.

## Round Completion Time

SSFL reduces transmission costs and communication overhead in SFL
training by employing parallel shards, which distribute the workload
across multiple nodes. BSFL incorporates blockchain technology to
enhance the security of the system, which, in turn, increases the
communication load due to committee member coordination and propagation
of updates to and from the blockchain. In our experiments, we evaluate
the round completion time of all training frameworks by measuring the
time between the start and the end of each round and cycle, calculating
the computation as well as the communication overhead for each round.
This evaluation helps with identifying the most suitable distributed
learning method by considering specific constraints, such as time,
infrastructure, and other critical factors.

Figure [4](#fig:transmission){reference-type="ref"
reference="fig:transmission"} presents the transmission costs for each
algorithm discussed. SSFL achieves significantly lower computation time
compared to SL and SFL. BSFL incurs higher round completion time than
SSFL because of its committee consensus mechanism and blockchain-based
communication. However, BSFL compensates for this overhead with faster
convergence, resulting in substantially lower overall training time
compared to SL and SFL. Table
[\[tab:performance_comparison\]](#tab:performance_comparison){reference-type="ref"
reference="tab:performance_comparison"} displays the average round
completion time for each algorithm, demonstrating that even without
applying early stopping, BSFL maintains $11\%$ and $10\%$ lower average
round completion time than SL and SFL, respectively, showcasing its
efficiency and adaptability in secure distributed learning setups.

# Future Works

In the following, we discuss three directions to enhance the scalability
and evaluation mechanisms of the proposed solution by exploring other
variations of split learning and adapting evaluation metrics.

[]{#sec:future-works label="sec:future-works"}

## SL variations

An alternative approach to implementing SL and its variations, including
SFL, involves splitting the model into three or more parts. In this
configuration, the last few layers are also trained locally by clients,
eliminating the need to share batch targets with the SL server. In this
study, we only split the model into two parts; however, both SSFL and
BSFL can be extended to support multi-part model splits. Such an
extension could improve client-side privacy and reduce data exposure
while maintaining the framework's scalability and performance.
Nevertheless, this setup increases the computational power demanded from
the clients since they must contribute to the training of more layers.
This trade-off encourages further assessment from the distributed
learning research community.

## Evaluation Metric

Lastly, the evaluation mechanism can be adapted to metrics beyond
traditional losses, especially for generative applications where labels
are not required for assessing model performance. In these scenarios,
metrics such as Feature Likelihood Divergence (FLD)
[@jiralerspong2024feature] or Fréchet Inception Distance (FID)
[@heusel2017gans] can be employed. These metrics are particularly
relevant for evaluating nodes in tasks involving generative models,
offering better insights into their performance.

# Conclusion {#sec:conclusion}

In this paper, we introduced two new enhanced SplitFed Learning (SFL)
frameworks called Sharded SplitFed Learning (SSFL) and
Blockchian-enabled SplitFed Learning. SSFL addresses the scalability
problem of SFL by distributing the workload of the SL server across
multiple shards. Meanwhile, BSFL enhances the security and stability of
the system by replacing the centralized server with a blockchain
network. This network leverages a committee consensus mechanism with an
evaluation process that prevents the aggregation of harmful model
updates. We validated the effectiveness of our proposed frameworks
through extensive experiments, comparing them with existing SL
algorithms under various settings. Our results showcase the improvement
in scalability, security, and convergence time for both SSFL and BSFL.

[^1]:
    The following link provides the implementation code in an
    anonymous GitHub repository to maintain the double-blinding
    constraint: **https://github.com/icdcs249/SSFL-BSFL**
