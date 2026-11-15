// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * DAO Governance for AI Model Release
 *
 * Purpose:
 * Govern the release of AI model versions using member voting.
 *
 * AI computation is performed OFF-CHAIN.
 * Only the model version and SHA-256 manifest digest are stored on-chain.
 *
 * Governance rules:
 * - One registered member = one vote
 * - Quorum = 3 votes
 * - Proposal passes only when YES > NO
 * - A tie fails
 * - Voting must be closed before execution
 * - Proposals are uniquely identified by model version + manifest digest
 */

contract DAOGovernance {

    // ------------------------------------------------------------
    // ENUMS
    // ------------------------------------------------------------

    enum ProposalState {
        Pending,
        Active,
        Succeeded,
        Defeated,
        Queued,
        Executed,
        Cancelled
    }

    // ------------------------------------------------------------
    // STRUCTS
    // ------------------------------------------------------------

    struct Proposal {
        uint256 id;

        string modelVersion;

        // SHA-256 digest represented as a bytes32 value.
        bytes32 manifestDigest;

        uint256 startTime;
        uint256 endTime;

        uint256 yesVotes;
        uint256 noVotes;

        uint256 memberSnapshot;

        ProposalState state;

        bool executed;
        bool cancelled;
    }

    // ------------------------------------------------------------
    // STATE VARIABLES
    // ------------------------------------------------------------

    address public admin;

    bool public paused;

    uint256 public constant QUORUM = 3;

    uint256 public constant VOTING_DURATION = 2 minutes;

    uint256 private proposalCounter;

    uint256 public memberCount;

    mapping(address => bool) public isMember;

    mapping(uint256 => mapping(address => bool)) public hasVoted;

    mapping(uint256 => Proposal) public proposals;

    // Prevent the same model version + manifest digest
    // from being submitted more than once.
    mapping(bytes32 => bool) public proposalExists;

    // ------------------------------------------------------------
    // EVENTS
    // ------------------------------------------------------------

    event MemberRegistered(
        address indexed member
    );

    event MemberRemoved(
        address indexed member
    );

    event ProposalCreated(
        uint256 indexed proposalId,
        string modelVersion,
        bytes32 indexed manifestDigest,
        uint256 startTime,
        uint256 endTime,
        uint256 memberSnapshot
    );

    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bool support
    );

    event ProposalQueued(
        uint256 indexed proposalId
    );

    event ProposalExecuted(
        uint256 indexed proposalId
    );

    event ProposalCancelled(
        uint256 indexed proposalId
    );

    event EmergencyPause(
        bool paused
    );

    // ------------------------------------------------------------
    // MODIFIERS
    // ------------------------------------------------------------

    modifier onlyAdmin() {
        require(
            msg.sender == admin,
            "Only admin can perform this action"
        );
        _;
    }

    modifier whenNotPaused() {
        require(
            !paused,
            "DAO is paused"
        );
        _;
    }

    modifier proposalExistsCheck(uint256 proposalId) {
        require(
            proposalId > 0 && proposalId <= proposalCounter,
            "Proposal does not exist"
        );
        _;
    }

    // ------------------------------------------------------------
    // CONSTRUCTOR
    // ------------------------------------------------------------

    constructor() {
        admin = msg.sender;

        // The deployer is automatically the first member.
        isMember[msg.sender] = true;
        memberCount = 1;

        emit MemberRegistered(msg.sender);
    }

    // ------------------------------------------------------------
    // MEMBER MANAGEMENT
    // ------------------------------------------------------------

    function registerMember(
        address member
    )
        external
        onlyAdmin
        whenNotPaused
    {
        require(
            member != address(0),
            "Invalid member address"
        );

        require(
            !isMember[member],
            "Already a member"
        );

        isMember[member] = true;
        memberCount++;

        emit MemberRegistered(member);
    }

    function removeMember(
        address member
    )
        external
        onlyAdmin
        whenNotPaused
    {
        require(
            isMember[member],
            "Not a member"
        );

        require(
            member != admin,
            "Admin cannot be removed"
        );

        isMember[member] = false;
        memberCount--;

        emit MemberRemoved(member);
    }

    // ------------------------------------------------------------
    // PROPOSAL CREATION
    // ------------------------------------------------------------

    function createProposal(
        string calldata modelVersion,
        bytes32 manifestDigest
    )
        external
        onlyAdmin
        whenNotPaused
        returns (uint256)
    {
        require(
            bytes(modelVersion).length > 0,
            "Model version required"
        );

        require(
            manifestDigest != bytes32(0),
            "Manifest digest required"
        );

        require(
            memberCount >= QUORUM,
            "Not enough members for quorum"
        );

        // Create a unique key using model version + digest.
        bytes32 uniqueKey = keccak256(
            abi.encodePacked(
                modelVersion,
                manifestDigest
            )
        );

        require(
            !proposalExists[uniqueKey],
            "Duplicate proposal"
        );

        proposalCounter++;

        uint256 startTime = block.timestamp;
        uint256 endTime = startTime + VOTING_DURATION;

        proposals[proposalCounter] = Proposal({
            id: proposalCounter,
            modelVersion: modelVersion,
            manifestDigest: manifestDigest,
            startTime: startTime,
            endTime: endTime,
            yesVotes: 0,
            noVotes: 0,
            memberSnapshot: memberCount,
            state: ProposalState.Active,
            executed: false,
            cancelled: false
        });

        proposalExists[uniqueKey] = true;

        emit ProposalCreated(
            proposalCounter,
            modelVersion,
            manifestDigest,
            startTime,
            endTime,
            memberCount
        );

        return proposalCounter;
    }

    // ------------------------------------------------------------
    // VOTING
    // ------------------------------------------------------------

    function vote(
        uint256 proposalId,
        bool support
    )
        external
        whenNotPaused
        proposalExistsCheck(proposalId)
    {
        Proposal storage proposal = proposals[proposalId];

        require(
            isMember[msg.sender],
            "Only registered members can vote"
        );

        require(
            block.timestamp >= proposal.startTime,
            "Voting has not started"
        );

        require(
            block.timestamp <= proposal.endTime,
            "Voting has ended"
        );

        require(
            proposal.state == ProposalState.Active,
            "Proposal is not active"
        );

        require(
            !hasVoted[proposalId][msg.sender],
            "Member has already voted"
        );

        hasVoted[proposalId][msg.sender] = true;

        if (support) {
            proposal.yesVotes++;
        } else {
            proposal.noVotes++;
        }

        emit VoteCast(
            proposalId,
            msg.sender,
            support
        );
    }

    // ------------------------------------------------------------
    // FINALIZE PROPOSAL
    // ------------------------------------------------------------

    function finalizeProposal(
        uint256 proposalId
    )
        public
        proposalExistsCheck(proposalId)
    {
        Proposal storage proposal = proposals[proposalId];

        require(
            block.timestamp > proposal.endTime,
            "Voting is still active"
        );

        require(
            proposal.state == ProposalState.Active,
            "Proposal already finalized"
        );

        uint256 totalVotes =
            proposal.yesVotes +
            proposal.noVotes;

        // Quorum failure.
        if (totalVotes < QUORUM) {
            proposal.state = ProposalState.Defeated;
            return;
        }

        // Strict majority.
        // YES must be greater than NO.
        // Therefore a tie automatically fails.
        if (proposal.yesVotes > proposal.noVotes) {
            proposal.state = ProposalState.Succeeded;
        } else {
            proposal.state = ProposalState.Defeated;
        }
    }

    // ------------------------------------------------------------
    // QUEUE
    // ------------------------------------------------------------

    function queueProposal(
        uint256 proposalId
    )
        external
        onlyAdmin
        whenNotPaused
        proposalExistsCheck(proposalId)
    {
        Proposal storage proposal = proposals[proposalId];

        require(
            block.timestamp > proposal.endTime,
            "Voting is still active"
        );

        require(
            proposal.state == ProposalState.Succeeded,
            "Proposal did not succeed"
        );

        proposal.state = ProposalState.Queued;

        emit ProposalQueued(proposalId);
    }

    // ------------------------------------------------------------
    // EXECUTION
    // ------------------------------------------------------------

    function executeProposal(
        uint256 proposalId
    )
        external
        onlyAdmin
        whenNotPaused
        proposalExistsCheck(proposalId)
    {
        Proposal storage proposal = proposals[proposalId];

        require(
            proposal.state == ProposalState.Queued,
            "Proposal is not queued"
        );

        require(
            block.timestamp > proposal.endTime,
            "Voting must be closed"
        );

        require(
            !proposal.executed,
            "Proposal already executed"
        );

        proposal.executed = true;
        proposal.state = ProposalState.Executed;

        emit ProposalExecuted(proposalId);
    }

    // ------------------------------------------------------------
    // CANCELLATION
    // ------------------------------------------------------------

    function cancelProposal(
        uint256 proposalId
    )
        external
        onlyAdmin
        proposalExistsCheck(proposalId)
    {
        Proposal storage proposal = proposals[proposalId];

        require(
            !proposal.executed,
            "Executed proposal cannot be cancelled"
        );

        require(
            proposal.state != ProposalState.Cancelled,
            "Already cancelled"
        );

        proposal.cancelled = true;
        proposal.state = ProposalState.Cancelled;

        emit ProposalCancelled(proposalId);
    }

    // ------------------------------------------------------------
    // EMERGENCY PAUSE
    // ------------------------------------------------------------

    function setEmergencyPause(
        bool pauseStatus
    )
        external
        onlyAdmin
    {
        paused = pauseStatus;

        emit EmergencyPause(
            pauseStatus
        );
    }

    // ------------------------------------------------------------
    // VIEW FUNCTIONS
    // ------------------------------------------------------------

    function getProposal(
        uint256 proposalId
    )
        external
        view
        proposalExistsCheck(proposalId)
        returns (
            uint256 id,
            string memory modelVersion,
            bytes32 manifestDigest,
            uint256 startTime,
            uint256 endTime,
            uint256 yesVotes,
            uint256 noVotes,
            uint256 memberSnapshot,
            ProposalState state,
            bool executed,
            bool cancelled
        )
    {
        Proposal memory proposal =
            proposals[proposalId];

        return (
            proposal.id,
            proposal.modelVersion,
            proposal.manifestDigest,
            proposal.startTime,
            proposal.endTime,
            proposal.yesVotes,
            proposal.noVotes,
            proposal.memberSnapshot,
            proposal.state,
            proposal.executed,
            proposal.cancelled
        );
    }

    function getProposalCount()
        external
        view
        returns (uint256)
    {
        return proposalCounter;
    }

    function getTotalVotes(
        uint256 proposalId
    )
        external
        view
        proposalExistsCheck(proposalId)
        returns (uint256)
    {
        Proposal memory proposal =
            proposals[proposalId];

        return proposal.yesVotes + proposal.noVotes;
    }

    function quorumReached(
        uint256 proposalId
    )
        external
        view
        proposalExistsCheck(proposalId)
        returns (bool)
    {
        Proposal memory proposal =
            proposals[proposalId];

        return (
            proposal.yesVotes +
            proposal.noVotes >= QUORUM
        );
    }
}