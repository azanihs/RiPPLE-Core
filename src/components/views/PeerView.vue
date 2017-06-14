<template>
            <md-tabs md-fixed class="tabScope">
                <md-tab id="BEAMENTOR" md-label="BE A MENTOR">
                    <md-layout md-gutter="16" md-flex="100">
                        <md-layout md-flex="33" v-for="peer in peers" :key="peer.id">
                            <md-card md-with-hover class="peerCard">
                                <md-card-area>
                                    <md-card-media md-ratio="16:9">
                                        <img src="../../../assets/images.jpg" alt="Question image">
                                    </md-card-media>            

                                    <md-card-header>
                                        <h2 class="md-title">Student's name</h2>
                                        <div class="md-subhead">
                                            <md-icon>thumb_up</md-icon>
                                            <span>{{ peer.rating }}</span>
                                        </div>
                                    </md-card-header>

                                    <md-card-content>
                                        A brief discription about student.
                                    </md-card-content>
                                </md-card-area>

                                <div class = "palceAround">
                                    <md-card-content>
                                        <!--<h3 class="md-subheading">Availability</h3>-->
                                        <div class="card-reservation">
                                            <md-icon>access_time</md-icon>
                                            <md-button-toggle md-single class="md-button-group">
                                                <md-button>5:30PM</md-button>
                                                <md-button>7:30PM</md-button>
                                                <md-button>9:00PM</md-button>
                                                </md-button-toggle>
                                        </div>
                                    </md-card-content>
                                </div>
                                            
                                <div class="placeAround">
                                    <md-card-content>
                                        <span><md-chip class="topicChip">{{ peer.topic }}</md-chip></span>
                                    </md-card-content>
                                    <md-card-actions>
                                        <md-button class="md-primary">Send Request</md-button>
                                    </md-card-actions>
                                </div>

                            </md-card>
                        </md-layout>
                    </md-layout>
                </md-tab>

                <md-tab id="NeedMentor" md-label="NEED A MENTOR">
                   <md-layout md-gutter="16" md-flex="100">
                        <md-layout md-flex="33" v-for="peer in peers" :key="peer.id">
                            <md-card md-with-hover class="peerCard">
                                <md-card-area md-inset>
                                    <md-card-media md-ratio="16:9">
                                        <img src="../../../assets/images2.jpg" alt="Question image">
                                    </md-card-media>            

                                    <md-card-header>
                                        <h2 class="md-title">Student's name</h2>
                                        <div class="md-subhead">
                                            <md-icon>thumb_up</md-icon>
                                            <span>{{ peer.rating }}</span>
                                        </div>
                                    </md-card-header>

                                    <md-card-content>
                                        A brief discription about student.
                                    </md-card-content>
                                </md-card-area>

                                <div class = "palceAround">
                                    <md-card-content>
                                        <!--<h3 class="md-subheading">Availability</h3>-->
                                        <div class="card-reservation">
                                            <md-icon>access_time</md-icon>
                                            <md-button-toggle md-single class="md-button-group">
                                                <md-button>5:30PM</md-button>
                                                <md-button>7:30PM</md-button>
                                                <md-button>9:00PM</md-button>
                                                </md-button-toggle>
                                        </div>
                                    </md-card-content>
                                </div>
                                            
                                <div class="placeAround">
                                    <md-card-content>
                                        <span><md-chip class="topicChip">{{ peer.topic }}</md-chip></span>
                                    </md-card-content>
                                    <md-card-actions>
                                        <md-button class="md-primary">Send Request</md-button>
                                    </md-card-actions>
                                </div>

                            </md-card>
                        </md-layout>
                    </md-layout>
                </md-tab>

                <md-tab id="studyPeer" md-label="STUDY PEER">
                    <md-layout md-gutter="16" md-flex="100">
                        <md-layout md-flex="33" v-for="peer in peers" :key="peer.id">
                            <md-card md-with-hover class="peerCard">
                                <md-card-area md-inset>
                                    <md-card-media md-ratio="16:9">
                                        <img src="../../../assets/images3.jpg" alt="Question image">
                                    </md-card-media>            

                                    <md-card-header>
                                        <h2 class="md-title">Student's name</h2>
                                        <div class="md-subhead">
                                            <md-icon>thumb_up</md-icon>
                                            <span>{{ peer.rating }}</span>
                                        </div>
                                    </md-card-header>

                                    <md-card-content>
                                        A brief discription about student.
                                    </md-card-content>
                                </md-card-area>

                                <div class = "palceAround">
                                    <md-card-content>
                                        <!--<h3 class="md-subheading">Availability</h3>-->
                                        <div class="card-reservation">
                                            <md-icon>access_time</md-icon>
                                            <md-button-toggle md-single class="md-button-group">
                                                <md-button>5:30PM</md-button>
                                                <md-button>7:30PM</md-button>
                                                <md-button>9:00PM</md-button>
                                                </md-button-toggle>
                                        </div>
                                    </md-card-content>
                                </div>
                                            
                                <div class="placeAround">
                                    <md-card-content>
                                        <span><md-chip class="topicChip">{{ peer.topic }}</md-chip></span>
                                    </md-card-content>
                                    <md-card-actions>
                                        <md-button class="md-primary">Send Request</md-button>
                                    </md-card-actions>
                                </div>

                            </md-card>
                        </md-layout>
                    </md-layout>
                </md-tab>
            </md-tabs>
</template>



<style scoped>
    .fullHeight {
        height: 100%;
    }
    .tabScope{
        min-width: 100%;
    }
    .headingContainer {
        border-bottom: 1px solid #222;
        margin: 8px;
	}	
	.competency {
        min-width: 100%;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .cardContainer {
        margin: 8px;
        flex: 1;
    }
    .peerCard {
        min-width: 100px;
        margin-top: 8px;
        margin-bottom: 8px;
    }
    .md-button {
      border-radius: 2px !important;
    }
    .questionCard .actions {
        justify-content: space-between;
    }
    .topicChip:hover {
        background-color: #333;
    }
    .placeAround {
        justify-content: space-between !important;
        display: flex;
        padding-bottom: 0px;
        align-items: center;
    }
    .placeAround > span {
        cursor: pointer;
    }
</style>

<script lang="ts">

    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionRepository from "@/repositories/QuestionRepository";
    import PeerRepository from "@/repositories/PeerRepository";


    @Component()
    export default class PeerView extends Vue {
        peers = null;
        studyPeers = null;

        @Lifecycle
        created() {
            this.peers = PeerRepository.getMulti(5);
        }
    }
    

</script>
