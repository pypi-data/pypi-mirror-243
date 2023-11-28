
from pymodaq_plugins_piezoconcept.hardware.piezoconcept.piezoconcept import PiezoConceptPI, Position, Time
from pymodaq_plugins_piezoconcept.daq_move_plugins.daq_move_PiezoConcept import DAQ_Move_PiezoConcept, main, comon_parameters_fun


class DAQ_Move_PiezoConceptPI(DAQ_Move_PiezoConcept):
    """
    Plugin to drive piezoconcpet XY (Z) stages. There is a string nonlinear offset between the set position and the read
    position. It seems to bnot be problem in the sens where a given displacement is maintained. But because the read
    position is not "accurate", I've decided to ignore it and just trust the set position. So the return will be always
    strictly equal to the set position. However, if there is more that 10% difference raise a warning
    """

    def ini_attributes(self):
        self.controller: PiezoConceptPI = None

    def ini_stage(self, controller=None):
        """

        """

        self.ini_stage_init(old_controller=controller,
                            new_controller=PiezoConceptPI())

        controller_id = self.do_init()

        info = controller_id
        initialized = True
        return info, initialized


    def get_actuator_value(self):
        """
            Check the current position from the hardware.

            Returns
            -------
            float
                The position of the hardware.

            See Also
            --------
            DAQ_Move_base.get_position_with_scaling, daq_utils.ThreadCommand
        """
        position = self.controller.get_position(self.settings.child('multiaxes', 'axis').value())  #in
        if position.unit == 'n':
            pos = position.pos/1000  # in um
        else:
            pos = position.pos
        pos = self.get_position_with_scaling(pos)
        self.current_position = self.target_position  #should be pos but not precise enough conpared to set position
        #print(pos)
        return self.target_position


if __name__ == '__main__':
    main(__file__, init=False)

