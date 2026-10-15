#include "../src/motion.h"
#include <cassert>
#include <iostream>
int main() {
    smoothui::Motion m;
    smoothui::Box a{10,10,80,40},b{100,10,105,40},c{220,10,60,40};
    m.set(a,1000,true);assert(m.sample(1000)==a);assert(!m.active(1000));
    m.set(b,2000,false);assert(m.sample(2000)==a);
    auto mid=m.sample(42000);assert(mid.x>a.x && mid.x<b.x);assert(mid.w>a.w && mid.w<b.w);
    assert(m.active(81000));assert(m.sample(82000)==b);assert(!m.active(82000));
    m.set(c,140000,false);auto before=m.sample(190000);
    m.set(a,190000,false);assert(m.sample(190000)==before);assert(m.sample(320000)==a);
    m.set(c,330000,true);assert(m.sample(330000)==c);assert(!m.active(330000));
    m.reset();m.set(a,340000,false);assert(m.sample(340000)==a);assert(!m.active(340000));
    std::cout<<"PASS: 80 ms interpolation, width change, interruption continuity, typing reset, no overshoot\n";
}
