from brownie import config, network, Vote
from scripts.utils import get_account


def deploy_voting_contract():
    account = get_account()
    vote = Vote.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    # starting voting
    start_voting_tx = vote.startvoting({"from": account})
    start_voting_tx.wait(1)
    return vote


def voteCandidateA():
    account = get_account()
    vote = deploy_voting_contract()
    vote_candidate_A = vote.voteCandidateA(
        {"from": account},
    )
    vote_candidate_A.wait(1)


def main():
    deploy_voting_contract()
    voteCandidateA()
