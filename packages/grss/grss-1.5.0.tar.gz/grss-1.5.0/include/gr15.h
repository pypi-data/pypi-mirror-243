#ifndef GR15_H
#define GR15_H

#include "approach.h"

const real hVec[8] = {
    0.0,
    0.0562625605369221464656521910318,
    0.180240691736892364987579942780,
    0.352624717113169637373907769648,
    0.547153626330555383001448554766,
    0.734210177215410531523210605558,
    0.885320946839095768090359771030,
    0.977520613561287501891174488626
};
const real rMat[8][8] = {
    {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {17.773808914078000840752659565672904106978971632681, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {5.5481367185372165056928216140765061758579336941398, 8.0659386483818866885371256689687154412267416180207, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {2.8358760786444386782520104428042437400879003147949, 3.3742499769626352599420358188267460448330087696743, 5.8010015592640614823286778893918880155743979164251, 0.0, 0.0, 0.0, 0.0, 0.0},
    {1.8276402675175978297946077587371204385651628457154, 2.0371118353585847827949159161566554921841792590404, 2.7254422118082262837742722003491334729711450288807, 5.1406241058109342286363199091504437929335189668304, 0.0, 0.0, 0.0, 0.0},
    {1.3620078160624694969370006292445650994197371928318, 1.4750402175604115479218482480167404024740127431358, 1.8051535801402512604391147435448679586574414080693, 2.6206449263870350811541816031933074696730227729812, 5.34597689987110751412149096322778980457703366603548, 0.0, 0.0, 0.0},
    {1.1295338753367899027322861542728593509768148769105, 1.2061876660584456166252036299646227791474203527801, 1.4182782637347391537713783674858328433713640692518, 1.8772424961868100972169920283109658335427446084411, 2.9571160172904557478071040204245556508352776929762, 6.6176620137024244874471284891193925737033291491748, 0.0, 0.0},
    {1.0229963298234867458386119071939636779024159134103, 1.0854721939386423840467243172568913862030118679827, 1.2542646222818777659905422465868249586862369725826, 1.6002665494908162609916716949161150366323259154408, 2.3235983002196942228325345451091668073608955835034, 4.1099757783445590862385761824068782144723082633980, 10.846026190236844684706431007823415424143683137181, 0.0}
};
const real cMat[8][8] = {
    {1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {-0.562625605369221464656522e-1, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {0.1014080283006362998648180399549641417413495311078e-1, -0.2365032522738145114532321e0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0},
    {-0.35758977292516175949344589284567187362040464593728e-2, 0.9353769525946206589574845561035371499343547051116e-1, -0.5891279693869841488271399e0, 1, 0, 0, 0, 0},
    {0.19565654099472210769005672379668610648179838140913e-2, -0.54755386889068686440808430671055022602028382584495e-1, 0.41588120008230686168862193041156933067050816537030e0, -0.11362815957175395318285885e1, 1, 0, 0, 0},
    {-0.14365302363708915424459554194153247134438571962198e-2, 0.42158527721268707707297347813203202980228135395858e-1, -0.36009959650205681228976647408968845289781580280782e0, 0.12501507118406910258505441186857527694077565516084e1, -0.18704917729329500633517991e1, 1, 0, 0},
    {0.12717903090268677492943117622964220889484666147501e-2, -0.38760357915906770369904626849901899108502158354383e-1, 0.36096224345284598322533983078129066420907893718190e0, -0.14668842084004269643701553461378480148761655599754e1, 0.29061362593084293014237914371173946705384212479246e1, -0.27558127197720458314421589e1, 1, 0},
    {-0.12432012432012432012432013849038719237133940238163e-2, 0.39160839160839160839160841227582657239289159887563e-1, -0.39160839160839160839160841545895262429018228668896e0, 0.17948717948717948717948719027866738711862551337629e1, -0.43076923076923076923076925231853900723503338586335e1, 0.56000000000000000000000001961129300233768803845526e1, -0.37333333333333333333333334e1, 1}
};
const real rVec[28] = {
    0.0562625605369221464656522,
    0.1802406917368923649875799, 0.1239781311999702185219278,
    0.3526247171131696373739078, 0.2963621565762474909082556, 0.1723840253762772723863278,
    0.5471536263305553830014486, 0.4908910657936332365357964, 0.3669129345936630180138686, 0.1945289092173857456275408,
    0.7342101772154105315232106, 0.6779476166784883850575584, 0.5539694854785181665356307, 0.3815854601022408941493028, 0.1870565508848551485217621,
    0.8853209468390957680903598, 0.8290583863021736216247076, 0.7050802551022034031027798, 0.5326962297259261307164520, 0.3381673205085403850889112, 0.1511107696236852365671492,
    0.9775206135612875018911745, 0.9212580530243653554255223, 0.7972799218243951369035945, 0.6248958964481178645172667, 0.4303669872307321188897259, 0.2433104363458769703679639, 0.0921996667221917338008147
};
const real cVec[21] = {
    -0.0562625605369221464656522,
    0.01014080283006362998648180399549641417413495311078, -0.2365032522738145114532321,
    -0.0035758977292516175949344589284567187362040464593728, 0.09353769525946206589574845561035371499343547051116, -0.5891279693869841488271399,
    0.0019565654099472210769005672379668610648179838140913, -0.054755386889068686440808430671055022602028382584495, 0.41588120008230686168862193041156933067050816537030, -1.1362815957175395318285885,
    -0.0014365302363708915424459554194153247134438571962198, 0.042158527721268707707297347813203202980228135395858, -0.36009959650205681228976647408968845289781580280782, 1.2501507118406910258505441186857527694077565516084, -1.8704917729329500633517991,
    0.001271790309026867749294311762296422088948466147501, -0.038760357915906770369904626849901899108502158354383, 0.36096224345284598322533983078129066420907893718190, -1.4668842084004269643701553461378480148761655599754, 2.9061362593084293014237914371173946705384212479246, -2.7558127197720458314421589
};
const real dVec[21] = {
    0.0562625605369221464656522,
    0.0031654757181708292499905, 0.2365032522738145114532321,
    0.0001780977692217433881125, 0.0457929855060279188954539, 0.5891279693869841488271399,
    0.0000100202365223291272096, 0.0084318571535257015445000, 0.2535340690545692665214616, 1.1362815957175395318285885,
    0.0000005637641639318207610, 0.0015297840025004658189490, 0.0978342365324440053653648, 0.8752546646840910912297246, 1.8704917729329500633517991,
    0.0000000317188154017613665, 0.0002762930909826476593130, 0.0360285539837364596003871, 0.5767330002770787313544596, 2.2485887607691597933926895, 2.7558127197720458314421588
};

real get_initial_timestep(propSimulation *propSim);
void update_g_with_b(const std::vector<std::vector<real>> &b, const size_t &dim, real *g);
void compute_g_and_b(const std::vector<std::vector<real> > &AccIntegArr,
                     const size_t &hIdx, real *g, real *bCompCoeffs,
                     std::vector<std::vector<real> > &b, const size_t &dim);
void refine_b(std::vector<std::vector<real> > &b, real *e, const real &dtRatio,
              const size_t &dim);
void check_and_apply_events(propSimulation *propSim, const real &t,
                            real &tNextEvent, size_t &nextEventIdx,
                            std::vector<real> &xInteg);
void gr15(propSimulation *propSim);

#endif
