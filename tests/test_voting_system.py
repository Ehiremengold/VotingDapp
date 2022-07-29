from brownie import Vote, network, exceptions
from scripts.utils import get_account, local_dev_env
from scripts.deploy import deploy_voting_contract
import pytest


def test_voting_is_closed():
    if network.show_active() not in local_dev_env:
        pytest.skip("for local testing only")
    account = get_account()
    non_account = get_account(index=1)  # another user
    vote = Vote.deploy({"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        vote.voteCandidateA({"from": account})


def test_only_owner_can_open_voting():
    if network.show_active() not in local_dev_env:
        pytest.skip("for local testing only")
    account = get_account()
    non_account = get_account(index=1)  # another user
    vote = Vote.deploy({"from": account})
    with pytest.raises(exceptions.VirtualMachineError):
        vote.startvoting({"from": non_account})


def test_voting_a_candidate():
    if network.show_active() not in local_dev_env:
        pytest.skip("for local testing only")
    account = get_account()
    another_account = get_account(index=2)
    vote = Vote.deploy({"from": account})
    opening_voting_tx = vote.startvoting({"from": account})
    opening_voting_tx.wait(1)
    # voter 1
    voting_tx = vote.voteCandidateA({"from": account})
    voting_tx.wait(1)
    # voter 2
    voting_tx = vote.voteCandidateA({"from": another_account})
    voting_tx.wait(1)
    assert vote.candidatesAVoteCount() == 2


def test_user_state_after_voting():
    if network.show_active() not in local_dev_env:
        pytest.skip("for local testing only")
    account = get_account()
    another_account = get_account(index=2)
    vote = Vote.deploy({"from": account})
    opening_voting_tx = vote.startvoting({"from": account})
    opening_voting_tx.wait(1)
    # voter 1
    voting_tx = vote.voteCandidateA({"from": account})
    voting_tx.wait(1)
    assert vote.userToUserState(account) == True


def test_user_cannot_vote_twice():
    if network.show_active() not in local_dev_env:
        pytest.skip("for local testing only")
    account = get_account()
    another_account = get_account(index=2)
    vote = Vote.deploy({"from": account})
    opening_voting_tx = vote.startvoting({"from": account})
    opening_voting_tx.wait(1)
    # voter 1
    voting_tx = vote.voteCandidateA({"from": account})
    voting_tx.wait(1)
    with pytest.raises(exceptions.VirtualMachineError):
        voting_2_tx = vote.voteCandidateB({"from": account})
        voting_2_tx.wait(1)


def test_total_votes():
    account = get_account()
    account_two = get_account(index=2)
    account_three = get_account(index=4)
    vote = deploy_voting_contract()
    # vote candidate A
    voting_candidateA_tx = vote.voteCandidateA({"from": account})
    voting_candidateA_tx.wait(1)
    # vote candidate B
    voting_candidateB_tx = vote.voteCandidateB({"from": account_two})
    voting_candidateB_tx.wait(1)
    # vote candidate C
    voting_candidateC_tx = vote.voteCandidateC({"from": account_three})
    voting_candidateC_tx.wait(1)
    assert vote.totalVoters({"from": account}) == 3
