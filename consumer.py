import logging
import time
import threading

from sdc11073.consumer.consumerimpl import HttpServerThreadBase
from sdc11073 import wsdiscovery
from sdc11073 import loghelper
from sdc11073.consumer import SdcConsumer
from sdc11073.mdib.consumermdib import ConsumerMdib


logging.basicConfig(level=logging.INFO)


patient_data = {
    "status": "Disconnected",
    "heart_rate": 0,
    "systolic_bp": 0,
    "diastolic_bp": 0,
    "spo2": 0
}






def find_provider():

    print("Searching Provider...")


    try:

        wsd = wsdiscovery.WSDiscovery(
            "192.168.0.20"
        )


        wsd.start()


        services = wsd.search_services(
            timeout=5
        )


        wsd.stop()



        if len(services) == 0:

            return None



        return services[0]



    except Exception as e:

        print(
            "Discovery error:",
            e
        )

        return None






def connect_provider():


    while True:


        try:


            service = find_provider()



            if service is None:


                print("Provider Not Found")


                patient_data["status"] = "Provider Not Found"


                time.sleep(5)


                continue




            print("Provider Found")



            sdc = SdcConsumer.from_wsd_service(

                service,

                ssl_context_container=None

            )


            print("SDC Consumer Created")




            logger = loghelper.get_logger_adapter(
                "consumer"
            )



            http_server = HttpServerThreadBase(

                "192.168.0.20",

                None,

                [],

                logger

            )



            http_server.start()



            while http_server.httpd is None:

                time.sleep(0.1)



            print("Consumer HTTP Server Started")

            print(
                "Port:",
                http_server.my_port
            )




            sdc.start_all(

                shared_http_server=http_server

            )



            print("Connected Successfully")



            patient_data["status"] = "Connected"




            mdib = ConsumerMdib(sdc)



            mdib.init_mdib()

           # mdib.process_incoming_metric_states_report = on_metric_update

            print("MDIB Loaded")
            for s in mdib.states.objects:
                print(type(s))
                print(s)
            while True:

                try:

                    for state in mdib.states.objects:

                        if not hasattr(state, "MetricValue"):
                            continue

                        if state.MetricValue is None:
                            continue

                        value = state.MetricValue.Value

                        print("Handle:", state.DescriptorHandle)
                        print("Value :", value)
                        print("----------------")

                        handle = state.DescriptorHandle

                        if handle == "metric1":
                            patient_data["heart_rate"] = value

                        elif handle == "metric2":
                            patient_data["spo2"] = value

                        elif handle == "metric3":
                            patient_data["systolic_bp"] = value
                    time.sleep(1)

                except Exception as e:
                    print(e)
                    time.sleep(1)


            print("Available Metrics:")



            for descriptor in mdib.descriptions.objects:


                if descriptor.is_metric_descriptor:


                    print(
                        descriptor.NODETYPE.localname
                    )




            #
            # attach metric callback
            #

            sdc.on_metric_report = on_metric_update



            print("Waiting Live Data...")



            while True:

                time.sleep(1)



        except Exception:

            import traceback

            traceback.print_exc()


            patient_data["status"] = "Disconnected"



        time.sleep(5)







def start_consumer():


    thread = threading.Thread(

        target=connect_provider,

        daemon=True

    )


    thread.start()
