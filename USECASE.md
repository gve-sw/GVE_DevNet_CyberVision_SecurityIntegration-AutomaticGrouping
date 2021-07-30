Cyber Vision Security and Automated Components Grouping
=====================================

This python application provides the following features/solution:
 
* **Task 1**: It retrieves domains/public IPs from cyber vision and checks them against Cisco Umbrella (or integrated 3rd party platform) to get their reputation. For any malicious domain or IP detected, an event is pushed to Cyber Vision dashboard to notify the user.

* **Task 2**: It auto-groups components. A group here is a logical collection of components that share certain characteristic. When Cisco Cyber Vision is deployed in an environment, it detects the components connected. To reduce the manual work of grouping components, this applications automatically groups ungrouped components according to vendor. A further development of the project could also automatically group components by subnet or tags.

- **A screenshot of the events after a Malicious domain is found**
![sample events](/IMAGES/img1.png)


- **A screenshot of Grooups automatically created and components assigned to them**
![sample groups](/IMAGES/img2.png)

## Related Sandbox

[Cyber Vision DevNet Sandbox](https://devnetsandbox.cisco.com/RM/Diagram/Index/8c568eeb-6f33-4aca-b661-2342518107d0?diagramType=Topology)

## Links to DevNet Learning Labs

[Cyber Vision Learning Lab](https://developer.cisco.com/learning/lab/iot-cybervision-getting-started/step/1)
