import xml.etree.ElementTree as ET


def parse_si_xml(si_xml_path):
    """Parse the si.xml file and print GPU and CPU names."""
    si_tree = ET.parse(si_xml_path)
    si_root = si_tree.getroot()
    motherboard_info = si_root.find("./Motherboard_Info")
    monitor_name = si_root.find('.DirectX_Info/DXGI/Adapter/Output/DeviceString')
    monitor_res_width = si_root.find('.DirectX_Info/DXGI/Adapter/Output/PhysicalWidth')
    monitor_res_height = si_root.find('.DirectX_Info/DXGI/Adapter/Output/PhysicalHeight')
    gpu_name = si_root.find('./Direct_Query_Info/GPU')
    gpu_driver_ver = si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_VER')
    gpu_driver_date = si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_DATE')
    gpu_driver_name = si_root.find('./GPUZ_Info/GPUs/GPU/DRIVER_NAME_NICE')
    cpu_name = si_root.find('./Direct_Query_Info/CPU')
    os_ver = si_root.find('./Direct_Query_Info/OS')
    memory_quantity = si_root.find('./Direct_Query_Info/Memory')
    memory_slots = si_root.findall('.//Memory_Slot')
    motherboard_manufacturer = si_root.find('./Motherboard_Info/Manufacturer')
    motherboard_model = si_root.find('./Motherboard_Info/Model')
    motherboard_ver = si_root.find('./Motherboard_Info/Version')
    motherboard_bios_date = si_root.find('./Motherboard_Info/BIOS_Release_Date')

    # Initialize variables
    populated_slots_count = 0
    frequencies = []

    print("System Info:\n")
    print("Monitor (one used for the benchmark):", monitor_name.text if monitor_name is not None else "Not found")
    print("Monitor Resolution:", monitor_res_width.text if monitor_res_width is not None else "Not found", "X",
          monitor_res_height.text if monitor_res_height is not None else "Not found")
    print("CPU Name:", cpu_name.text if cpu_name is not None else "Not found")
    print("GPU Name:", gpu_name.text if gpu_name is not None else "Not found")
    print("GPU Driver Name:", gpu_driver_name.text if gpu_driver_name is not None else "Not found")
    print("GPU Driver Version:", gpu_driver_ver.text if gpu_driver_ver is not None else "Not found")
    print("GPU Driver Release Date:", gpu_driver_date.text if gpu_driver_date is not None else "Not found")
    print("OS:", os_ver.text if os_ver is not None else "Not found")

    for slot in memory_slots:
        # Check if the slot has a non-zero Capacity
        capacity_element = slot.find('Capacity')
        if capacity_element is not None:
            capacity_value = float(capacity_element.find('DoubleValue').text)
            if capacity_value > 0:
                populated_slots_count += 1

                # Extract the frequency
                frequency_element = slot.find('Frequency')
                if frequency_element is not None:
                    frequency_value = float(frequency_element.find('DoubleValue').text) * 1000
                    frequencies.append(frequency_value)

    if memory_quantity is not None and memory_quantity.text is not None:
        try:
            memory_int = int(memory_quantity.text.strip())
            print("Memory:", memory_int // 1024, "GB (", memory_int // 1024 // populated_slots_count, "GB X",
                  populated_slots_count, ")")
        except ValueError:
            print("Memory: Could not convert to integer")
    else:
        print("Memory: Not found")
    print("Memory Frequency:", frequencies)

    print("\nMotherboard Info: \n")
    print("Manufacturer:", motherboard_manufacturer.text if motherboard_manufacturer is not None else "Not found")
    print("Model:", motherboard_model.text if motherboard_model is not None else "Not found")
    print("Board Version:", motherboard_ver.text if motherboard_ver is not None else "Not found")

    version_elements = motherboard_info.findall('Version')
    if len(version_elements) > 1:
        specific_version = version_elements[1].text
        print("BIOS Version:", specific_version)
    else:
        print("No second 'Version' element found.")

    print("BIOS Release Date:", motherboard_bios_date.text if motherboard_bios_date is not None else "Not found")


def parse_arielle_xml(arielle_xml_path):
    """Parse the arielle.xml file and print test results."""
    ari_tree = ET.parse(arielle_xml_path)
    ari_root = ari_tree.getroot()

    dandia_loop_done = dandia_fps_stability = dandia_test_pass = None

    for result in ari_root.findall('./results/result'):
        name = result.find('name').text
        value = float(result.find('value').text)
        if name == 'DandiaLoopDoneXST':
            dandia_loop_done = value
        elif name == 'DandiaFpsStabilityXST':
            dandia_fps_stability = value
        elif name == 'DandiaTestPassXST':
            dandia_test_pass = value

    if dandia_test_pass is not None:
        print("\nTest Passed!\nPass Summary List:" if dandia_test_pass == 1.0 else "\nTest Failed!\nFail Summary List:")
    else:
        print("DandiaTestPassXST not found. Cannot determine overall test result.")

    if dandia_loop_done is not None:
        print(
            f"Loops Completed (DandiaLoopDoneXST): {dandia_loop_done} (Pass)" if dandia_loop_done >= 20 else f"Loops Completed (DandiaLoopDoneXST): {dandia_loop_done} (Fail)")
    else:
        print("Loops Completed (DandiaLoopDoneXST) not found.")

    if dandia_fps_stability is not None:
        print(
            f"Frame Rate Stability (DandiaFpsStabilityXST): {dandia_fps_stability / 10}% (Pass)" if dandia_fps_stability >= 970.0 else f"Frame Rate Stability (DandiaFpsStabilityXST): {dandia_fps_stability / 10}% (Fail. Must be >= 97.0%)")
    else:
        print("Frame Rate Stability (DandiaFpsStabilityXST) not found.")

    fps_values = []
    print("\nIndividual FPS Values:")
    for idx, result in enumerate(ari_root.findall('.//result'), start=1):
        primary_result = result.find('./primary_result')
        if primary_result is not None and primary_result.get('unit') == 'fps':
            fps_value = round(float(primary_result.text), 2)
            fps_values.append((idx, fps_value))
            print(f"Loop {idx}: {fps_value} fps")

    if fps_values:
        average_fps = round(sum(fps for idx, fps in fps_values) / len(fps_values), 2)
        print(f"\nAverage FPS: {average_fps} fps")

        best_fps_idx, best_fps = max(fps_values, key=lambda x: x[1])
        worst_fps_idx, worst_fps = min(fps_values, key=lambda x: x[1])

        print(f"Best Individual Loop: Loop {best_fps_idx} with {best_fps} fps")
        print(f"Worst Individual Loop: Loop {worst_fps_idx} with {worst_fps} fps")

        margin = round(((best_fps / worst_fps) * 100 - 100), 2)
        print("Margin Between Best and Worst Runs: " + str(margin) + " %\n")
