:image: https://raw.githubusercontent.com/Tobi-De/falco/main/assets/og-image.jpg
:description: MISSING_DESCRIPTION

Building extensible software
============================

When I say extensible here, I don't mean, writing clean code or using design patterns to make you code easily modifyable. Nor I'm a 
a talking about building a JSON based API aka rest API to build for people to easily extends or use your system. What I'm talking about
here is writing software (in our case django projects) in a way that external people to your team can build external module to your
project that can easily be integrate to existing instance of your project without having to change your original code (this is important)
to be able to add new features to your features or extends existing ones. THis is commonly done via the plugin architecture, the best example 
I've found on this in the python ecosystem are odoo, baserom, django-cms and especially pretix, the last one being the main inspiration
for this guide. Pretix is open source and I borrowed a lot for their code this guide, It is code worth fidling with. So Full credits to the 
pretix team for the approach I'm going to showcase.

Disclaimer haven't built a similiar system myself yet in prod

Additional ressources
---------------------

- the pretix repository
- the talk on the plugin architecture

From all the codebase I've read through, there seems be too main approach to integrate the plugin architectur in a dkango project, one is the autodiscovery approach and the seconds is the registry approach, bot are not mutual exclusive, you can have both approach and w'll see a bit of both. But a good idea is to keep focus on a specific, if not these can become a confusing fast if there is a lot of different options to extends your software. Pretix is a bit on the autodiscovery aspects.

So before even diving deep, I want to list what seems to be the most important aspects of making somtething like this work

- having a lot of conventions, conventions over configurations
- documentation, document a lot of things
- a bit of magic seems to be acceptable here, if it make the plugin development experience better