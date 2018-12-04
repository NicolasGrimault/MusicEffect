import sox

REVERB = "reverb"
ECHO = "echo"
CHORUS = "chorus"


def getTransformer(request):
    tfm = sox.Transformer()
    if request.form.getlist(REVERB):
        hfd = float(request.form.get(REVERB + '_high_freq_damping', 50))
        rsc = float(request.form.get(REVERB + '_room_scale', 100))
        rev = float(request.form.get(REVERB + '_reverberance', 50))
        tfm.reverb(reverberance=rev, high_freq_damping=hfd, room_scale=rsc)
    if request.form.getlist(ECHO):
        gin = float(request.form.get(ECHO + '_gain_in', 0.8))
        gou = float(request.form.get(ECHO + '_gain_out', 0.9))
        # Todo need to parse list of float
        # nec = int(request.form.get('echo_n_echos',1))
        # dea = request.form.get('echo_delays',[60])
        # dec = request.form.get('echo_decays',[0.4])
        tfm.echo(gain_in=gin, gain_out=gou)
    if request.form.getlist(CHORUS):
        gin = float(request.form.get(CHORUS + '_gain_in', 0.3))
        gou = float(request.form.get(CHORUS + '_gain_out', 0.8))
        nvo = int(request.form.get(CHORUS + '_n_voices', 3))
        tfm.chorus(gain_in=gin, gain_out=gou, n_voices=nvo)

    return tfm
