################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time, math
from Leap import CircleGesture, SwipeGesture

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    thumbsupcounter = 0
    circlemotioncounter = 0
    swipeupcounter = 0
    swipedowncounter = 0
    heartcounter = 0
    gesture = ""

    def getGesture(self):
        # self.gesture = None
        return self.gesture

    def resetGesture(self):
        self.gesture = ""

    def resetCounters(self):
        self.circlemotioncounter = 0
        self.swipeupcounter = 0
        self.swipedowncounter = 0
        self.thumbsupcounter = 0
        self.heartcounter = 0

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()

        # print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
            #   frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        if len(frame.hands) == 0:
            # print 'No hands detected'
            # print self.thumbsupcounter, self.circlemotioncounter, self.swipeupcounter, self.swipedowncounter
            self.resetCounters()
            return None

        pointable = frame.pointables.frontmost
        speed = pointable.tip_velocity
        if speed[2] > 800:
            self.thumbsupcounter = 0
        # print speed[2]
            self.swipeupcounter += 1
        if speed[2] < -800:
            self.thumbsupcounter = 0
            # print speed[2]
            self.swipedowncounter += 1

        if self.swipedowncounter == 10:
            # print "SWIPING UP"
            self.gesture = 'swipe_up'
            self.resetCounters()

        if self.swipeupcounter == 10:
            # print "SWIPING DOWN"
            self.gesture='swipe_down'
            self.resetCounters()

        # print "UP",self.swipedowncounter
        # print "DOWN",self.swipeupcounter

        hc = []
        # Get hands
        for hand in frame.hands:

            hc.append([hand.id,hand.palm_position[0],hand.palm_position[2]])

            handType = "Left hand" if hand.is_left else "Right hand"

            # print "  %s, id %d, position: %s" % (

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Get arm bone
            arm = hand.arm
            # print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (

            # Get fingers
            extended_count = 0
            fingerlist = {}
            for finger in hand.fingers:
                # if self.finger_names[finger.type] != 'Thumb':
                fingerlist[self.finger_names[finger.type]] = finger.is_extended
                # print "    %s finger, id: %d, length: %fmm, width: %fmm" % (

                if finger.is_extended == True:
                    extended_count+=1
                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    # print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                    #     self.bone_names[bone.type],
                    #     bone.prev_joint,
                    #     bone.next_joint,
                    #     bone.direction)

            if extended_count == 0 or extended_count == 1:
                self.thumbsupcounter += 1
            else:
                # print "NO thumbs up detected"
                self.thumbsupcounter = 0

            if self.thumbsupcounter == 66:
                # print 'Thumbs up detected!'
                # self.resetCounters()
                self.gesture = 'thumbsup'
                self.resetCounters()

        # print fingerlist
        # if fingerlist["Pinky"] == False and fingerlist["Index"] == False and fingerlist["Ring"] == False and fingerlist["Pinky"] == False and fingerlist["Thumb"] == True:
        #     print "thumbs up"
        # else:
        #     print 'no thumbs up'


        # for finger in fingerlist:
        #     print self.finger_names[finger.type]," is extended", finger.is_extended


        # Get gestures
        try:
            dx =  math.fabs(hc[0][1] - hc[1][1])
            dy =  math.fabs(hc[0][2] - hc[1][2])
            # print "delta x",dx
            # print "delta y",dy
            if dx < 220 and dy < 45:
                self.thumbsupcounter = 0
                self.heartcounter += 1
                # print self.heartcounter

                if self.heartcounter == 50:
                    self.gesture = 'heart'
                    self.resetCounters()
        except:
            pass


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"

def main():

    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
