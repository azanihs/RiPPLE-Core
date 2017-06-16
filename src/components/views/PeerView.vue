<template>
    <md-layout md-flex="95">
    <md-layout md-flex="100" class="headingContainer">
        <h1>Connect With Peers</h1>
        <availability-selector />
    </md-layout>
    <md-layout class="headingContainer">
        <h1>Review Recommendations</h1>
    </md-layout>
    <md-layout class="fullHeight" md-flex="100">
        <md-tabs md-fixed class="md-transparent">
            <md-tab id="BEAMENTOR" md-label="BE A MENTOR">
                <md-list>
                    <md-list-item>
                        <md-icon>school</md-icon>
                        <span>COMPETENCIES</span>

                        <md-list-expand>

                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>people</md-icon>
                        <span>RECOMMENDATIONS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard" md-theme="blue">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>5:30PM</md-button>
                                                            <md-button>7:30PM</md-button>
                                                            <md-button>9:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">CSS</md-chip>
                                                                <md-chip class="topicChip">THX</md-chip>
                                                                <md-chip class="topicChip">PCI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avator2.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sandra Brown</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>2:30PM</md-button>
                                                            <md-button>6:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">JSON</md-chip>
                                                                <md-chip class="topicChip">EXE</md-chip>
                                                                <md-chip class="topicChip">SSL</md-chip>
                                                                <md-chip class="topicChip">RAM</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sarah Watson</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>9:30AM</md-button>
                                                            <md-button>3:30PM</md-button>
                                                            <md-button>8:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">USB</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>person_add</md-icon>
                        <span>REQUESTS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>7:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SQL</md-chip>
                                                                <md-chip class="topicChip">SCSI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images3.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Jack Russel</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>4:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SMTP</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images2.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Niki Raol</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>11:30AM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">SQL</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
            </md-tab>

            <md-tab id="NeedMentor" md-label="NEED A MENTOR">
                <md-list>
                    <md-list-item>
                        <md-icon>school</md-icon>
                        <span>COMPETENCIES</span>

                        <md-list-expand>

                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>people</md-icon>
                        <span>RECOMMENDATIONS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard" md-theme="blue">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>5:30PM</md-button>
                                                            <md-button>7:30PM</md-button>
                                                            <md-button>9:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">CSS</md-chip>
                                                                <md-chip class="topicChip">THX</md-chip>
                                                                <md-chip class="topicChip">PCI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avator2.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sandra Brown</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>2:30PM</md-button>
                                                            <md-button>6:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">JSON</md-chip>
                                                                <md-chip class="topicChip">EXE</md-chip>
                                                                <md-chip class="topicChip">SSL</md-chip>
                                                                <md-chip class="topicChip">RAM</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sarah Watson</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>9:30AM</md-button>
                                                            <md-button>3:30PM</md-button>
                                                            <md-button>8:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">USB</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>person_add</md-icon>
                        <span>REQUESTS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>7:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SQL</md-chip>
                                                                <md-chip class="topicChip">SCSI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images3.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Jack Russel</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>4:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SMTP</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images2.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Niki Raol</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>11:30AM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">SQL</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
            </md-tab>

            <md-tab id="studyPeer" md-label="STUDY PEER">
                <md-list>
                    <md-list-item>
                        <md-icon>school</md-icon>
                        <span>COMPETENCIES</span>

                        <md-list-expand>

                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>people</md-icon>
                        <span>RECOMMENDATIONS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard" md-theme="blue">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>5:30PM</md-button>
                                                            <md-button>7:30PM</md-button>
                                                            <md-button>9:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">CSS</md-chip>
                                                                <md-chip class="topicChip">THX</md-chip>
                                                                <md-chip class="topicChip">PCI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avator2.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sandra Brown</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>2:30PM</md-button>
                                                            <md-button>6:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">JSON</md-chip>
                                                                <md-chip class="topicChip">EXE</md-chip>
                                                                <md-chip class="topicChip">SSL</md-chip>
                                                                <md-chip class="topicChip">RAM</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.png" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Sarah Watson</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>9:30AM</md-button>
                                                            <md-button>3:30PM</md-button>
                                                            <md-button>8:00PM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">USB</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
                <md-list>
                    <md-list-item>
                        <md-icon>person_add</md-icon>
                        <span>REQUESTS</span>

                        <md-list-expand>
                            <md-layout md-gutter="16" md-flex="100">
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/avatar.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Marcos Moura</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>7:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SQL</md-chip>
                                                                <md-chip class="topicChip">SCSI</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images3.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Jack Russel</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>4:30PM</md-button>
                                                        </md-button-toggle>
                                                        <span>
                                                                <md-chip class="topicChip">SMTP</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                                <md-layout md-flex="33">
                                    <md-card md-with-hover class="peerCard">
                                        <md-card-header>
                                            <md-avatar>
                                                <img src="../../../assets/images2.jpg" alt="People">
                                            </md-avatar>

                                            <md-card-expand>
                                                <md-card-actions>
                                                    <md-button>Niki Raol</md-button>
                                                    <span style="flex: 1"></span>
                                                    <md-button class="md-icon-button" md-expand-trigger>
                                                        <md-icon>keyboard_arrow_down</md-icon>
                                                    </md-button>
                                                </md-card-actions>

                                                <md-card-content>
                                                    A brief discription about student
                                                </md-card-content>
                                            </md-card-expand>
                                        </md-card-header>
                                        <md-card-area>
                                            <div class="palceAround">
                                                <md-card-content>
                                                    <div class="card-reservation">
                                                        <md-button-toggle md-single class="md-button-group">
                                                            <md-button>11:30AM</md-button>
                                                        </md-button-toggle>
                                                        <span><md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">RSS</md-chip>
                                                            <md-chip class="topicChip">SQL</md-chip>
                                                            </span>
                                                    </div>
                                                </md-card-content>
                                            </div>
                                        </md-card-area>
                                        <div>
                                            <md-card-area>
                                                <div class="placeAround">
                                                    <md-card-content>
                                                        <md-button class="md-primary">ignore</md-button>
                                                    </md-card-content>
                                                    <md-card-actions>
                                                        <md-button class="md-primary">Send Request</md-button>
                                                    </md-card-actions>
                                                </div>
                                            </md-card-area>
                                        </div>
                                    </md-card>
                                </md-layout>
                            </md-layout>
                        </md-list-expand>
                    </md-list-item>
                </md-list>
            </md-tab>
        </md-tabs>

    </md-layout>
    </md-layout>
</template>



<style scoped>
    hr {
        border: none;
        border-bottom: 1px solid #ccc;
    }
    .fullHeight {
        height: 100%;
    }
    .headingContainer {
        margin: 8px 0px 0px 0px;
	}

    .md-tabs {
        border-top: 1px solid rgba(0, 0, 0, .12);
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
        min-width: 40px;
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
    .iconClass{
        align-items: center;
        background-color: red;
    }

    .cardPreview img {
        width: 50%;
        height: auto;
        float: left;
        border: 1px solid #bbb;
        padding-right: 10px;
        padding-bottom: 10px;
        margin-right: 10px;
    }
</style>

<script lang="ts">

    import { Vue, Component, Lifecycle } from "av-ts";
    import QuestionRepository from "@/repositories/QuestionRepository";
    import PeerRepository from "@/repositories/PeerRepository";
    import AvailabilitySelector from "../util/AvailabilitySelector";

    @Component({
        components: {
            "availability-selector": AvailabilitySelector
        }
    })
    export default class PeerView extends Vue {
        peers = null;
        studyPeers = null;

        @Lifecycle
        created() {
            this.peers = PeerRepository.getMulti(3);
            this.studyPeers = PeerRepository.getMulti(5);
        }
    }
</script>
